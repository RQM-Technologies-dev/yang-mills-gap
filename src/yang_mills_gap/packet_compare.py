"""Compare diagnostic correlator/effective-mass packets."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Iterable

import numpy as np

from .packet_analysis import load_config, load_diagnostics, load_observables


def _load_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _finite_float(value: Any) -> float | None:
    if value in {"", None}:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if np.isfinite(number) else None


def _finite_stats(rows: list[dict[str, str]], key: str) -> tuple[float | str, int]:
    values = [_finite_float(row.get(key)) for row in rows]
    finite = [value for value in values if value is not None]
    if not finite:
        return "", 0
    return float(min(finite)), len(finite)


def summarize_effective_mass_packet(run_dir: str | Path) -> dict[str, Any]:
    """Return a compact summary for one correlator/effective-mass packet."""

    root = Path(run_dir)
    config = load_config(root)
    diagnostics = load_diagnostics(root)
    observables = load_observables(root)
    final_record = observables[-1] if observables else {}
    mass_rows = _load_csv_rows(root / "effective_mass.csv")
    min_log, n_log = _finite_stats(mass_rows, "m_eff_log")
    min_cosh, n_cosh = _finite_stats(mass_rows, "m_eff_cosh")
    summary = diagnostics.get("summary", {})
    return {
        "run_dir": str(root),
        "label": config.get("label", ""),
        "research_objective": config.get("research_objective", summary.get("research_objective", "")),
        "claim_boundary": config.get("claim_boundary", summary.get("claim_boundary", "")),
        "beta": config.get("beta", ""),
        "lattice_shape": tuple(config.get("lattice_shape", ())),
        "n_measurements": summary.get("n_measurements", len(observables)),
        "mean_acceptance_rate": summary.get("mean_acceptance_rate", ""),
        "final_average_plaquette": final_record.get("average_plaquette", ""),
        "final_average_closure_defect": final_record.get("average_closure_defect", ""),
        "min_finite_m_eff_log": min_log,
        "min_finite_m_eff_cosh": min_cosh,
        "n_finite_m_eff_log": n_log,
        "n_finite_m_eff_cosh": n_cosh,
    }


def compare_packet_summaries(packet_dirs: Iterable[str | Path]) -> list[dict[str, Any]]:
    """Return summaries for multiple packets."""

    return [summarize_effective_mass_packet(packet_dir) for packet_dir in packet_dirs]


def save_packet_comparison_csv(path: str | Path, summaries: Iterable[dict[str, Any]]) -> Path:
    """Write packet summaries to CSV."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [dict(summary) for summary in summaries]
    if not rows:
        raise ValueError("summaries must not be empty")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return output_path


def load_sweep_summary(sweep_dir: str | Path) -> list[dict[str, str]]:
    """Read ``sweep_summary.csv`` from a sweep directory if present."""

    return _load_csv_rows(Path(sweep_dir) / "sweep_summary.csv")
