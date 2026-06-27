import numpy as np

from yang_mills_gap.candidate import assess_closure_resonance_candidate


def test_assess_closure_resonance_candidate_flags_positive_plateau_with_warnings() -> None:
    artifacts = {
        "effective_mass_log": np.array([0.7, 0.71, 0.69]),
        "effective_mass_cosh": np.array([np.nan, np.nan]),
    }
    quality_gates = {"summary": {"n_fail": 0, "n_warn": 1}}

    assessment = assess_closure_resonance_candidate(artifacts, quality_gates)

    assert assessment["candidate_status"] == "candidate_with_warnings"
    assert assessment["selected_estimator"] == "log"
    assert assessment["candidate_mean"] > 0
    assert "finite-lattice" in assessment["claim_boundary"]


def test_assess_closure_resonance_candidate_blocks_failed_quality_gates() -> None:
    artifacts = {
        "effective_mass_log": np.array([0.7, 0.71, 0.69]),
        "effective_mass_cosh": np.array([np.nan, np.nan]),
    }
    quality_gates = {"summary": {"n_fail": 1, "n_warn": 0}}

    assessment = assess_closure_resonance_candidate(artifacts, quality_gates)

    assert assessment["candidate_status"] == "blocked_by_quality_gates"
    assert "quality gates have failed" in assessment["reasons"]


def test_assess_closure_resonance_candidate_rejects_missing_plateau() -> None:
    artifacts = {
        "effective_mass_log": np.array([np.nan, np.nan]),
        "effective_mass_cosh": np.array([np.nan, np.nan]),
    }
    quality_gates = {"summary": {"n_fail": 0, "n_warn": 0}}

    assessment = assess_closure_resonance_candidate(artifacts, quality_gates)

    assert assessment["candidate_status"] == "not_candidate"
    assert "no positive plateau candidate found" in assessment["reasons"]
