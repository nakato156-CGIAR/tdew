"""Unit tests for experiments.tcn.checkpoint.

Verifies a save/load roundtrip reproduces identical model/optimizer state,
and -- the property that actually matters for "resume training" -- that
interrupting training after step 1, saving, reloading into a fresh
model/optimizer, and continuing with step 2 gives bit-identical results to
never having been interrupted at all.
"""

from __future__ import annotations

from pathlib import Path

import torch

from experiments.tcn import checkpoint as ckpt
from tdew_estimation.models.tcn_attention import TCNAttentionConfig, TCNAttentionModel


def _fixed_batch(config: TCNAttentionConfig, context_length: int = 14, batch_size: int = 4):
    generator = torch.Generator().manual_seed(123)
    dynamic = torch.randn(batch_size, context_length, config.n_dynamic_features, generator=generator)
    static = torch.randn(batch_size, config.n_static_features, generator=generator)
    region = torch.arange(batch_size) % 3
    target_cond = torch.randn(batch_size, config.n_target_cond_features, generator=generator)
    label = torch.randn(batch_size, generator=generator)
    return dynamic, static, region, target_cond, label


def _small_config() -> TCNAttentionConfig:
    # dropout=0.0: keeps the forward pass deterministic given fixed weights
    # and fixed input, isolating the checkpoint/resume mechanics from any
    # unrelated dropout-RNG bookkeeping.
    return TCNAttentionConfig(d_model=16, n_tcn_blocks=3, n_attention_heads=2, dropout=0.0)


def _train_step(model, optimizer, batch) -> float:
    dynamic, static, region, target_cond, label = batch
    optimizer.zero_grad(set_to_none=True)
    pred = model(dynamic, static, region, target_cond)
    loss = torch.nn.functional.mse_loss(pred, label)
    loss.backward()
    optimizer.step()
    return float(loss.item())


def test_save_load_roundtrip_preserves_state(tmp_path: Path):
    torch.manual_seed(0)
    config = _small_config()
    model = TCNAttentionModel(config)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    batch = _fixed_batch(config)
    _train_step(model, optimizer, batch)  # give the optimizer some state (Adam moments)

    path = tmp_path / "ckpt.pt"
    ckpt.save_checkpoint(
        path,
        model=model,
        optimizer=optimizer,
        scheduler=None,
        epoch=0,
        global_step=1,
        best_val_skill=0.1,
        config={"d_model": config.d_model},
        mlflow_run_id="abc123",
    )
    assert path.exists()

    loaded = ckpt.load_checkpoint(path)
    assert loaded["epoch"] == 0
    assert loaded["global_step"] == 1
    assert loaded["best_val_skill"] == 0.1
    assert loaded["mlflow_run_id"] == "abc123"

    fresh_model = TCNAttentionModel(config)
    fresh_optimizer = torch.optim.AdamW(fresh_model.parameters(), lr=1e-3)
    ckpt.restore_into(loaded, model=fresh_model, optimizer=fresh_optimizer)

    for (name_a, param_a), (name_b, param_b) in zip(model.named_parameters(), fresh_model.named_parameters()):
        assert name_a == name_b
        assert torch.equal(param_a, param_b), f"{name_a} did not roundtrip exactly"

    for group_a, group_b in zip(optimizer.state_dict()["state"].values(), fresh_optimizer.state_dict()["state"].values()):
        assert torch.equal(group_a["exp_avg"], group_b["exp_avg"])
        assert torch.equal(group_a["exp_avg_sq"], group_b["exp_avg_sq"])


def test_resume_continues_training_identically(tmp_path: Path):
    config = _small_config()
    batch1 = _fixed_batch(config)  # same fixed data reused for both "steps" (isolates the RNG question)
    batch2_seed = 456

    def make_batch2():
        generator = torch.Generator().manual_seed(batch2_seed)
        dynamic = torch.randn(4, 14, config.n_dynamic_features, generator=generator)
        static = torch.randn(4, config.n_static_features, generator=generator)
        region = torch.arange(4) % 3
        target_cond = torch.randn(4, config.n_target_cond_features, generator=generator)
        label = torch.randn(4, generator=generator)
        return dynamic, static, region, target_cond, label

    batch2 = make_batch2()

    # --- Baseline: uninterrupted training for 2 steps. ---
    torch.manual_seed(0)
    model = TCNAttentionModel(config)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    _train_step(model, optimizer, batch1)
    baseline_loss_step2 = _train_step(model, optimizer, batch2)

    # --- Interrupted: train step 1, checkpoint, load into a fresh model/optimizer, continue with step 2. ---
    torch.manual_seed(0)
    model_a = TCNAttentionModel(config)
    optimizer_a = torch.optim.AdamW(model_a.parameters(), lr=1e-3)
    _train_step(model_a, optimizer_a, batch1)

    path = tmp_path / "resume.pt"
    ckpt.save_checkpoint(
        path,
        model=model_a,
        optimizer=optimizer_a,
        scheduler=None,
        epoch=0,
        global_step=1,
        best_val_skill=float("-inf"),
        config={},
    )

    torch.manual_seed(999)  # deliberately different seed: resume must not depend on it
    model_b = TCNAttentionModel(config)
    optimizer_b = torch.optim.AdamW(model_b.parameters(), lr=1e-3)
    loaded = ckpt.load_checkpoint(path)
    ckpt.restore_into(loaded, model=model_b, optimizer=optimizer_b)
    resumed_loss_step2 = _train_step(model_b, optimizer_b, batch2)

    assert abs(resumed_loss_step2 - baseline_loss_step2) < 1e-6
