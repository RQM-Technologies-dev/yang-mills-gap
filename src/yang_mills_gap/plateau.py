"""Simple effective-mass plateau heuristics.

These helpers are diagnostics only. They flag finite windows that look roughly
flat by a relative standard-deviation rule; they do not establish a physical
mass gap or replace finite-size, autocorrelation, and uncertainty analysis.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def finite_runs(values: np.ndarray) -> list[tuple[int, int]]:
    """Return inclusive index ranges for contiguous finite segments."""

    array = np.asarray(values, dtype=float)
    runs: list[tuple[int, int]] = []
    start: int | None = None
    for index, value in enumerate(array):
        if np.isfinite(value):
            if start is None:
                start = index
        elif start is not None:
            runs.append((start, index - 1))
            start = None
    if start is not None:
        runs.append((start, array.size - 1))
    return runs


def _relative_std(window: np.ndarray) -> float:
    mean = float(np.mean(window))
    std = float(np.std(window))
    scale = max(abs(mean), 1.0e-12)
    return std / scale


def plateau_candidates(
    values: np.ndarray,
    min_length: int = 2,
    relative_tolerance: float = 0.25,
) -> list[tuple[int, int]]:
    """Return inclusive finite windows that satisfy a flatness heuristic."""

    if min_length <= 0:
        raise ValueError("min_length must be positive")
    if relative_tolerance < 0.0:
        raise ValueError("relative_tolerance must be nonnegative")

    array = np.asarray(values, dtype=float)
    candidates: list[tuple[int, int]] = []
    for run_start, run_end in finite_runs(array):
        run_length = run_end - run_start + 1
        if run_length < min_length:
            continue
        for start in range(run_start, run_end - min_length + 2):
            for end in range(start + min_length - 1, run_end + 1):
                window = array[start : end + 1]
                if _relative_std(window) <= relative_tolerance:
                    candidates.append((start, end))
    return candidates


def summarize_plateau_candidates(
    values: np.ndarray,
    min_length: int = 2,
    relative_tolerance: float = 0.25,
) -> list[dict[str, Any]]:
    """Return CSV-safe summaries for candidate plateau windows."""

    array = np.asarray(values, dtype=float)
    summaries: list[dict[str, Any]] = []
    for start, end in plateau_candidates(array, min_length=min_length, relative_tolerance=relative_tolerance):
        window = array[start : end + 1]
        mean = float(np.mean(window))
        std = float(np.std(window))
        summaries.append(
            {
                "start_t": int(start),
                "end_t": int(end),
                "length": int(end - start + 1),
                "mean": mean,
                "std": std,
                "relative_std": _relative_std(window),
            }
        )
    return summaries
