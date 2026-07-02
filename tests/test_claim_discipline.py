from pathlib import Path

from yang_mills_gap.baseline_contract import BASELINE_CLAIM_BOUNDARY, BASELINE_DYNAMICS
from yang_mills_gap.candidate import CANDIDATE_CLAIM_BOUNDARY
from yang_mills_gap.quality_gates import QUALITY_GATE_CLAIM_BOUNDARY

ROOT = Path(__file__).resolve().parents[1]


def _read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_main_roadmap_surfaces_keep_finite_lattice_claim_boundary() -> None:
    surfaces = {
        "README.md": (
            "conjecture program",
            "Hamiltonian-gap-independent closure-energy definition",
        ),
        "ROADMAP.md": ("conjecture-oriented", "finite-lattice outputs"),
        "docs/09_curvature_closure_proof.md": (
            "central conjectural mechanism",
            "Hamiltonian-gap-independent",
        ),
        "docs/10_closure_coercivity_lemma.md": (
            "Closure energy, vacuum isolation",
            "independent of the spectral-gap conclusion",
        ),
        "docs/07_proof_roadmap.md": (
            "computational sandbox and conjecture-auditing environment",
            "Gap Register",
        ),
        "CLAIM_DISCIPLINE.md": (
            "conjecture program",
            "Hamiltonian-gap-independent closure-energy target",
        ),
    }

    for relative_path, required_phrases in surfaces.items():
        text = _read(relative_path)
        for phrase in required_phrases:
            assert phrase in text


def test_public_surfaces_avoid_overloaded_non_circular_wording() -> None:
    surfaces = [
        "README.md",
        "ROADMAP.md",
        "CLAIM_DISCIPLINE.md",
        "docs/09_curvature_closure_proof.md",
        "docs/10_closure_coercivity_lemma.md",
        "docs/07_proof_roadmap.md",
    ]
    forbidden_phrases = ("non-circular", "prevents circularity")

    for relative_path in surfaces:
        text = _read(relative_path).lower()
        for phrase in forbidden_phrases:
            assert phrase.lower() not in text


def test_public_research_surfaces_do_not_use_result_claim_language() -> None:
    surfaces = [
        "README.md",
        "ROADMAP.md",
        "docs/09_curvature_closure_proof.md",
        "docs/10_closure_coercivity_lemma.md",
        "docs/07_proof_roadmap.md",
    ]
    overclaims = (
        "establishes the Clay result",
        "settles the Millennium problem",
        "proves the Yang-Mills mass gap",
        "derives the continuum theorem",
    )

    for relative_path in surfaces:
        text = _read(relative_path)
        for phrase in overclaims:
            assert phrase not in text


def test_packet_claim_boundaries_remain_diagnostic_only() -> None:
    assert "diagnostic only" in BASELINE_CLAIM_BOUNDARY
    assert "not a mass-gap estimate" in BASELINE_CLAIM_BOUNDARY
    assert "no anchor or deformation term" in BASELINE_DYNAMICS
    assert "diagnostics only" in QUALITY_GATE_CLAIM_BOUNDARY
    assert "not mass-gap evidence" in QUALITY_GATE_CLAIM_BOUNDARY
    assert "diagnostic only" in CANDIDATE_CLAIM_BOUNDARY
    assert "not proof" in CANDIDATE_CLAIM_BOUNDARY


def test_no_links_to_removed_fragment_docs() -> None:
    removed = (
        "docs/00_problem_statement.md",
        "docs/01_rqm_mass_gap_hypothesis.md",
        "docs/02_su2_quaternionic_representation.md",
        "docs/03_lattice_yang_mills_baseline.md",
        "docs/04_closure_defect_and_wilson_action.md",
        "docs/05_glueball_correlator_mass_gap.md",
        "docs/06_rqm_anchor_deformations_nonstandard.md",
        "docs/08_closure_resonance_roadmap.md",
        "docs/finite_lattice_claim_boundary.md",
    )
    surfaces = (
        "README.md",
        "ROADMAP.md",
        "CLAIM_DISCIPLINE.md",
        "docs/07_proof_roadmap.md",
        "docs/09_curvature_closure_proof.md",
        "docs/10_closure_coercivity_lemma.md",
    )

    for relative_path in surfaces:
        text = _read(relative_path)
        for removed_path in removed:
            assert removed_path not in text


def test_anchor_deformation_code_keeps_nonstandard_boundary() -> None:
    text = _read("experiments/exp_006_rqm_anchor_deformation_nonstandard.py")

    assert "Quarantined nonstandard" in text
    assert "not part of the proof route" in text
    assert "not evidence" in text
