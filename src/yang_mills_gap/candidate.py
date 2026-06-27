"""Packet-level closure-resonance candidate assessment."""

from __future__ import annotations

from typing import Any

import numpy as np

from .plateau import summarize_plateau_candidates

CANDIDATE_CLAIM_BOUNDARY = "finite-lattice closure-resonance candidate diagnostic only; not proof of a mass gap"


def _finite_count(values: np.ndarray) -> int:
    return int(np.count_nonzero(np.isfinite(values)))


def _positive_plateaus(values: np.ndarray, estimator: str) -> list[dict[str, Any]]:
    plateaus = summarize_plateau_candidates(values)
    return [
        {
            "estimator": estimator,
            **plateau,
        }
        for plateau in plateaus
        if float(plateau["mean"]) > 0.0
    ]


def _best_plateau(candidates: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not candidates:
        return None
    return sorted(candidates, key=lambda item: (-int(item["length"]), float(item["relative_std"])))[0]


def assess_closure_resonance_candidate(
    artifacts: dict[str, np.ndarray],
    quality_gates: dict[str, Any],
    *,
    min_finite_effective_mass_values: int = 1,
) -> dict[str, Any]:
    """Assess whether one packet contains a finite-lattice candidate signal."""

    if min_finite_effective_mass_values <= 0:
        raise ValueError("min_finite_effective_mass_values must be positive")

    quality_summary = quality_gates.get("summary", {})
    n_quality_fail = int(quality_summary.get("n_fail", 0))
    n_quality_warn = int(quality_summary.get("n_warn", 0))
    mass_log = np.asarray(artifacts["effective_mass_log"], dtype=float)
    mass_cosh = np.asarray(artifacts["effective_mass_cosh"], dtype=float)
    finite_log_count = _finite_count(mass_log)
    finite_cosh_count = _finite_count(mass_cosh)
    finite_mass_count = finite_log_count + finite_cosh_count

    log_plateaus = _positive_plateaus(mass_log, "log")
    cosh_plateaus = _positive_plateaus(mass_cosh, "cosh")
    best = _best_plateau(cosh_plateaus + log_plateaus)

    reasons: list[str] = []
    if n_quality_fail:
        reasons.append("quality gates have failed")
    if finite_mass_count < min_finite_effective_mass_values:
        reasons.append("not enough finite effective-mass values")
    if best is None:
        reasons.append("no positive plateau candidate found")

    if reasons:
        status = "blocked_by_quality_gates" if n_quality_fail else "not_candidate"
    else:
        status = "candidate_with_warnings" if n_quality_warn else "candidate"
        reasons.append("positive finite-lattice plateau candidate passed packet-level checks")

    selected = best or {}
    return {
        "candidate_status": status,
        "claim_boundary": CANDIDATE_CLAIM_BOUNDARY,
        "selected_estimator": selected.get("estimator", ""),
        "candidate_window_start_t": selected.get("start_t", ""),
        "candidate_window_end_t": selected.get("end_t", ""),
        "candidate_length": selected.get("length", ""),
        "candidate_mean": selected.get("mean", ""),
        "candidate_relative_std": selected.get("relative_std", ""),
        "n_log_plateau_candidates": len(log_plateaus),
        "n_cosh_plateau_candidates": len(cosh_plateaus),
        "finite_log_count": finite_log_count,
        "finite_cosh_count": finite_cosh_count,
        "quality_gate_fail_count": n_quality_fail,
        "quality_gate_warn_count": n_quality_warn,
        "reasons": reasons,
    }
