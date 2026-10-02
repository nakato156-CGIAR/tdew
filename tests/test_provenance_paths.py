"""Las rutas absolutas del registro llevan el prefijo del checkout que las escribio;
tras cambiar de checkout/worktree hay que reanclarlas bajo el repo actual."""
from __future__ import annotations

from pathlib import Path

from tdew_estimation.provenance import resolve_recorded_path


def test_relative_path_is_anchored_at_repo_root(tmp_path):
    assert resolve_recorded_path("reports/a.csv", repo_root=tmp_path) == (
        tmp_path / "reports" / "a.csv").resolve()


def test_absolute_path_from_another_checkout_is_reanchored_under_reports(tmp_path):
    other = "/home/x/Code/tdew/.claude/worktrees/wt/reports/timesfm_benchmark/m.csv"
    (tmp_path / "reports" / "timesfm_benchmark").mkdir(parents=True)
    (tmp_path / "reports" / "timesfm_benchmark" / "m.csv").write_text("x")
    assert resolve_recorded_path(other, repo_root=tmp_path) == (
        tmp_path / "reports" / "timesfm_benchmark" / "m.csv").resolve()


def test_absolute_path_outside_the_repo_without_reports_is_untouched(tmp_path):
    work = "/home/cvelasquez/tdew_timesfm/backtest_clean_timesfm/metrics_all.csv"
    assert resolve_recorded_path(work, repo_root=tmp_path) == Path(work).resolve()


def test_absolute_path_inside_the_repo_is_kept(tmp_path):
    inside = tmp_path / "reports" / "a.csv"
    assert resolve_recorded_path(str(inside), repo_root=tmp_path) == inside.resolve()


def test_external_path_with_a_reports_component_is_untouched_unless_target_exists(tmp_path):
    external = "/home/cvelasquez/tdew_timesfm/reports/out.csv"
    assert resolve_recorded_path(external, repo_root=tmp_path) == Path(external).resolve()


def test_reanchor_only_when_the_reanchored_file_exists(tmp_path):
    other = "/home/x/Code/tdew/reports/timesfm_benchmark/m.csv"
    assert resolve_recorded_path(other, repo_root=tmp_path) == Path(other).resolve()
    target = tmp_path / "reports" / "timesfm_benchmark" / "m.csv"
    target.parent.mkdir(parents=True)
    target.write_text("x")
    assert resolve_recorded_path(other, repo_root=tmp_path) == target.resolve()


def test_worktree_path_nested_inside_the_main_checkout_is_reanchored(tmp_path):
    wt = tmp_path / ".claude" / "worktrees" / "wt" / "reports" / "a.csv"
    target = tmp_path / "reports" / "a.csv"
    target.parent.mkdir(parents=True)
    target.write_text("x")
    assert resolve_recorded_path(str(wt), repo_root=tmp_path) == target.resolve()


def test_username_directory_named_reports_does_not_hijack_the_anchor(tmp_path):
    other = "/home/reports/Code/tdew/reports/timesfm_benchmark/m.csv"
    target = tmp_path / "reports" / "timesfm_benchmark" / "m.csv"
    target.parent.mkdir(parents=True)
    target.write_text("x")
    assert resolve_recorded_path(other, repo_root=tmp_path) == target.resolve()
