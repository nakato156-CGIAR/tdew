"""GPU mechanics smoke test for TCNAttentionModel (bead tdew-x46).

Not a training run against real data -- a few forward/backward steps on
synthetic tensors under bf16 autocast on the actual RTX A2000, checking the
GPU path (autocast, TF32, cudnn.benchmark) doesn't produce NaN/Inf and that
a checkpoint saved from CUDA state reloads correctly. Skipped automatically
on machines without a CUDA GPU (e.g. CI).
"""

from __future__ import annotations

from pathlib import Path

import pytest
import torch

from experiments.tcn import checkpoint as ckpt
from experiments.tcn.train import configure_gpu
from tdew_estimation.models.losses import weighted_huber_loss
from tdew_estimation.models.tcn_attention import TCNAttentionConfig, TCNAttentionModel

requires_cuda = pytest.mark.skipif(not torch.cuda.is_available(), reason="no CUDA GPU available")


@requires_cuda
def test_bf16_autocast_forward_backward_is_finite(tmp_path: Path):
    configure_gpu()
    device = torch.device("cuda")
    config = TCNAttentionConfig()  # full-size default (~157K params)
    model = TCNAttentionModel(config).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

    batch_size, context_length = 512, 60  # largest frozen L; exercises the biggest attention matrix
    torch.manual_seed(0)
    dynamic = torch.randn(batch_size, context_length, config.n_dynamic_features, device=device)
    static = torch.randn(batch_size, config.n_static_features, device=device)
    region = torch.randint(0, 3, (batch_size,), device=device)
    target_cond = torch.randn(batch_size, config.n_target_cond_features, device=device)
    label = torch.randn(batch_size, device=device)
    weight = torch.rand(batch_size, device=device) + 0.1

    for step in range(3):
        optimizer.zero_grad(set_to_none=True)
        with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
            pred = model(dynamic, static, region, target_cond)
            loss = weighted_huber_loss(pred, label, weight, delta=1.0)
        assert torch.isfinite(loss), f"non-finite loss at step {step}"
        loss.backward()
        for name, param in model.named_parameters():
            if param.grad is not None:
                assert torch.isfinite(param.grad).all(), f"non-finite grad in {name} at step {step}"
        optimizer.step()

    # Checkpoint roundtrip from CUDA state.
    path = tmp_path / "gpu_ckpt.pt"
    ckpt.save_checkpoint(
        path,
        model=model,
        optimizer=optimizer,
        scheduler=None,
        epoch=0,
        global_step=3,
        best_val_skill=0.0,
        config={},
    )
    reloaded = TCNAttentionModel(config).to(device)
    reloaded_optimizer = torch.optim.AdamW(reloaded.parameters(), lr=1e-3)
    loaded = ckpt.load_checkpoint(path)  # CPU-mapped by default; load_state_dict moves it onto the GPU model/optimizer
    ckpt.restore_into(loaded, model=reloaded, optimizer=reloaded_optimizer)
    for (name_a, p_a), (name_b, p_b) in zip(model.named_parameters(), reloaded.named_parameters()):
        assert name_a == name_b
        assert torch.equal(p_a, p_b)


@requires_cuda
def test_batch_size_1024_fits_comfortably_in_12gb():
    """Sanity check for the design's batch-size recommendation: a full
    forward+backward at batch_size=1024, L=60 should use a small fraction of
    the A2000's 12GB, leaving headroom (matches the O(batch*heads*T^2)
    estimate in the design plan)."""
    configure_gpu()
    device = torch.device("cuda")
    torch.cuda.reset_peak_memory_stats(device)
    config = TCNAttentionConfig()
    model = TCNAttentionModel(config).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

    batch_size, context_length = 1024, 60
    dynamic = torch.randn(batch_size, context_length, config.n_dynamic_features, device=device)
    static = torch.randn(batch_size, config.n_static_features, device=device)
    region = torch.randint(0, 3, (batch_size,), device=device)
    target_cond = torch.randn(batch_size, config.n_target_cond_features, device=device)
    label = torch.randn(batch_size, device=device)
    weight = torch.ones(batch_size, device=device)

    optimizer.zero_grad(set_to_none=True)
    with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
        pred = model(dynamic, static, region, target_cond)
        loss = weighted_huber_loss(pred, label, weight)
    loss.backward()
    optimizer.step()

    peak_gb = torch.cuda.max_memory_allocated(device) / 1e9
    assert peak_gb < 2.0, f"unexpectedly high peak memory for batch=1024: {peak_gb:.2f} GB"
