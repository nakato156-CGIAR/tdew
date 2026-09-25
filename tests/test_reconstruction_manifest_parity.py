"""Parity check: docs/protocol/reconstruction_manifest.yaml vs. the hardcoded
ProtocolSpec values in experiments/reconstruction/protocol.py.

protocol.py duplicates the manifest's dates/panel sizes as a frozen dataclass
instead of loading the YAML at import time, so nothing else keeps the two in
sync. This test is the tripwire: edit one without the other and it fails.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

from experiments.reconstruction.protocol import Protocol, protocol_spec

MANIFEST_PATH = (
    Path(__file__).resolve().parents[1] / "docs" / "protocol" / "reconstruction_manifest.yaml"
)


def _manifest_protocols() -> dict:
    return yaml.safe_load(MANIFEST_PATH.read_text())["protocols"]


def test_manifest_protocols_cover_every_protocol_enum_member():
    manifest = _manifest_protocols()
    assert set(manifest) == {protocol.value for protocol in Protocol}


def test_protocol_spec_matches_manifest_for_every_protocol():
    manifest = _manifest_protocols()
    for protocol in Protocol:
        entry = manifest[protocol.value]
        spec = protocol_spec(protocol)

        train_start_year, train_end_year = entry["train"]
        hidden_start_year, hidden_end_year = entry["hidden"]

        assert spec.train_start == pd.Timestamp(f"{train_start_year}-01-01")
        assert spec.train_end == pd.Timestamp(f"{train_end_year}-12-31")
        assert spec.hidden_start == pd.Timestamp(f"{hidden_start_year}-01-01")
        assert spec.hidden_end == pd.Timestamp(f"{hidden_end_year}-12-31")
        assert spec.panel_cells_per_department == entry["panel_cells_per_department"]
        assert spec.sealed == entry.get("sealed", False)
