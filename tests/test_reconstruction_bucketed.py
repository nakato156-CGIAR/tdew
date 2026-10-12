from __future__ import annotations

import json

import pandas as pd
import pytest

from experiments.reconstruction.bucketed import (
    build_canonical_bucket,
    load_canonical_input,
    materialize_silver_buckets,
)


def test_bucketed_reader_only_opens_panel_buckets(tmp_path):
    root = tmp_path / "canonical"
    for bucket_id, location_id in ((1, 1), (2, 2)):
        target = root / f"id_bucket={bucket_id}" / "part.parquet"
        target.parent.mkdir(parents=True)
        pd.DataFrame(
            {"ID": [location_id], "date": [pd.Timestamp("2000-01-01")], "TMIN": [10.0]}
        ).to_parquet(target, index=False)
        # build_canonical_buckets leaves the audit sidecar next to the parquet.
        target.with_suffix(".json").write_text(json.dumps({"bucket_id": bucket_id}))
    (root / "manifest.json").write_text(
        json.dumps({"num_buckets": 8, "buckets": [{"bucket_id": 1}, {"bucket_id": 2}]})
    )
    result = load_canonical_input(root, ids=[1])
    assert result["ID"].tolist() == [1]
    assert "id_bucket" not in result



def test_canonical_join_refuses_a_bucket_count_that_differs_from_the_historical_layout(tmp_path):
    # The historical root is partitioned with 256 buckets, so bucket 3 holds
    # 3 and 259. Rebucketing silver with 8192 would silently drop 259.
    historical = tmp_path / "historical"
    target = historical / "id_bucket=0003" / "part.parquet"
    target.parent.mkdir(parents=True)
    pd.DataFrame(
        {
            "ID": [3, 259],
            "FECHA": [pd.Timestamp("2002-01-01")] * 2,
            "TD": [8.0, 9.0],
            "TMIN": [10.0, 11.0],
        }
    ).to_parquet(target, index=False)

    spatial = pd.DataFrame({"ID": [3, 259], "department": ["Lima"] * 2})
    empty_lst = pd.DataFrame({"ID": [], "month": []})
    with pytest.raises(ValueError, match="was not written with 8192 buckets"):
        build_canonical_bucket(
            3,
            historical_root=historical,
            silver_bucket_root=tmp_path / "silver",
            spatial=spatial,
            lst=empty_lst,
            num_buckets=8192,
        )

    canonical, metadata = build_canonical_bucket(
        3,
        historical_root=historical,
        silver_bucket_root=tmp_path / "silver",
        spatial=pd.DataFrame({"ID": [], "department": []}),
        lst=empty_lst,
        num_buckets=256,
    )
    assert canonical.empty and metadata["rows"] == 0


def test_rebucketing_groups_months_into_parts(tmp_path):
    silver = tmp_path / "silver"
    for month in range(1, 7):
        target = silver / "tmin" / f"tmin_daily_1981_{month:02d}.parquet"
        target.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(
            {
                "ID": [1, 2],
                "date": [pd.Timestamp(f"1981-{month:02d}-01")] * 2,
                "value": [10.0, 11.0],
            }
        ).to_parquet(target, index=False)

    root = materialize_silver_buckets(
        silver, tmp_path / "buckets", num_buckets=8,
        variables=("tmin",), selected_ids=pd.Index([1]), months_per_part=3,
    )
    parts = sorted((root / "tmin" / "id_bucket=1").glob("*.parquet"))
    assert [path.name for path in parts] == [
        "tmin_daily_1981_01__tmin_daily_1981_03.parquet",
        "tmin_daily_1981_04__tmin_daily_1981_06.parquet",
    ]
    frame = pd.read_parquet(root / "tmin" / "id_bucket=1")
    assert frame["ID"].tolist() == [1] * 6
    assert not (root / "tmin" / "id_bucket=2").exists()
