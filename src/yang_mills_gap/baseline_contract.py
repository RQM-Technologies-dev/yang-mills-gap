"""Contract helpers for the standard SU(2) Wilson-action baseline."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Final

from .observables import GLUEBALL_OPERATOR_MODES

BASELINE_NAME: Final = "standard SU(2) Wilson action only"
BASELINE_DYNAMICS: Final = "local Metropolis updates using the Wilson action; no anchor or deformation term"
BASELINE_CLAIM_BOUNDARY: Final = "finite-lattice diagnostic only; not a mass-gap estimate"
BASELINE_RESEARCH_OBJECTIVE: Final = "build auditable finite-lattice diagnostics for the closure-resonance working hypothesis"

FORBIDDEN_BASELINE_CONFIG_KEYS: Final = frozenset(
    {
        "anchor_strength",
        "anchor_term",
        "deformation",
        "deformation_strength",
        "target_defect",
    }
)


def validate_baseline_operator(operator: str) -> str:
    """Return a baseline measurement operator name or raise ``ValueError``."""

    if operator not in GLUEBALL_OPERATOR_MODES:
        raise ValueError(f"unknown glueball_operator: {operator}")
    return operator


def baseline_metadata(*, glueball_operator: str = "spatial_plaquette") -> dict[str, str]:
    """Return packet metadata for a standard Wilson-action baseline run."""

    return {
        "baseline": BASELINE_NAME,
        "baseline_dynamics": BASELINE_DYNAMICS,
        "claim_boundary": BASELINE_CLAIM_BOUNDARY,
        "research_objective": BASELINE_RESEARCH_OBJECTIVE,
        "glueball_operator": validate_baseline_operator(glueball_operator),
    }


def validate_baseline_sweep_config(config: Mapping[str, Any]) -> None:
    """Validate that a sweep config stays inside the local Wilson baseline."""

    forbidden_keys = FORBIDDEN_BASELINE_CONFIG_KEYS.intersection(config)
    if forbidden_keys:
        names = ", ".join(sorted(forbidden_keys))
        raise ValueError(f"baseline config contains nonstandard deformation keys: {names}")
    if config.get("baseline") != BASELINE_NAME:
        raise ValueError(f"baseline must be {BASELINE_NAME!r}")
    if config.get("claim_boundary") != BASELINE_CLAIM_BOUNDARY:
        raise ValueError(f"claim_boundary must be {BASELINE_CLAIM_BOUNDARY!r}")
    if config.get("research_objective") != BASELINE_RESEARCH_OBJECTIVE:
        raise ValueError(f"research_objective must be {BASELINE_RESEARCH_OBJECTIVE!r}")
    if config.get("use_local_action") is not True:
        raise ValueError("baseline sweep packets require use_local_action=True")
    validate_baseline_operator(str(config.get("glueball_operator", "")))
