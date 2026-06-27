from pathlib import Path

from yang_mills_gap.baseline_contract import BASELINE_CLAIM_BOUNDARY, BASELINE_DYNAMICS
from yang_mills_gap.candidate import CANDIDATE_CLAIM_BOUNDARY
from yang_mills_gap.quality_gates import QUALITY_GATE_CLAIM_BOUNDARY

ROOT = Path(__file__).resolve().parents[1]


def _read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_main_roadmap_surfaces_keep_finite_lattice_claim_boundary() -> None:
    surfaces = {
        "README.md": ("not a Clay", "not a continuum proof"),
        "ROADMAP.md": ("non-proof diagnostics", "finite-lattice diagnostics"),
        "docs/08_closure_resonance_roadmap.md": ("not a Clay", "finite-lattice diagnostic"),
        "docs/09_curvature_closure_proof.md": ("proof draft and research program", "not a completed Clay"),
        "docs/10_closure_coercivity_lemma.md": ("not a completed proof", "prevent circularity"),
        "docs/finite_lattice_claim_boundary.md": ("not a continuum construction", "do not by themselves establish"),
        "docs/07_proof_roadmap.md": ("computational sandbox, not a proof", "Gap Register"),
    }

    for relative_path, required_phrases in surfaces.items():
        text = _read(relative_path)
        for phrase in required_phrases:
            assert phrase in text


def test_public_research_surfaces_do_not_use_result_claim_language() -> None:
    surfaces = [
        "README.md",
        "ROADMAP.md",
        "docs/08_closure_resonance_roadmap.md",
        "docs/09_curvature_closure_proof.md",
        "docs/10_closure_coercivity_lemma.md",
        "docs/finite_lattice_claim_boundary.md",
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


def test_anchor_deformation_doc_keeps_nonstandard_boundary() -> None:
    text = _read("docs/06_rqm_anchor_deformations_nonstandard.md")

    assert "not part of standard SU(2) Wilson lattice Yang-Mills" in text
    assert "must be labeled nonstandard" in text
    assert "not evidence for a standard Yang-Mills mass-gap theorem" in text
