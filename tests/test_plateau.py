import numpy as np

from yang_mills_gap.plateau import finite_runs, plateau_candidates, summarize_plateau_candidates


def test_finite_runs_segments_nan_gaps() -> None:
    values = np.array([np.nan, 1.0, 2.0, np.nan, 3.0, np.nan, 4.0, 5.0])

    assert finite_runs(values) == [(1, 2), (4, 4), (6, 7)]


def test_plateau_candidates_finds_flat_synthetic_window() -> None:
    values = np.array([np.nan, 1.0, 1.04, 1.02, np.nan, 2.0, 3.0])

    candidates = plateau_candidates(values, min_length=3, relative_tolerance=0.05)

    assert (1, 3) in candidates


def test_plateau_candidates_rejects_nonflat_synthetic_window() -> None:
    values = np.array([1.0, 2.0, 4.0, 8.0])

    assert plateau_candidates(values, min_length=3, relative_tolerance=0.05) == []


def test_summarize_plateau_candidates_returns_csv_safe_dicts() -> None:
    values = np.array([0.9, 1.0, 1.1])

    summaries = summarize_plateau_candidates(values, min_length=3, relative_tolerance=0.1)

    assert summaries
    assert summaries[0]["start_t"] == 0
    assert summaries[0]["end_t"] == 2
    assert summaries[0]["length"] == 3
    assert isinstance(summaries[0]["mean"], float)
    assert isinstance(summaries[0]["relative_std"], float)
