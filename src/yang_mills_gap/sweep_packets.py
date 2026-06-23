"""Helpers for beta/seed diagnostic packet sweeps."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import numpy as np

from .gauge_field import GaugeField
from .lattice import Lattice4D
from .monte_carlo import metropolis_sweep_local
from .observables import average_closure_defect, average_plaquette, glueball_timeseries
from .packet_compare import compare_packet_summaries, save_packet_comparison_csv
from .run_packet import save_config_json, save_manifest_json, save_records_csv
from .spectroscopy_packet import write_correlator_packet
from .wilson_action import wilson_action


DEFAULT_RESEARCH_OBJECTIVE = "build auditable finite-lattice diagnostics for the closure-resonance working hypothesis"
DEFAULT_CLAIM_BOUNDARY = "finite-lattice diagnostic only; not a mass-gap estimate"


def create_sweep_dir(base_dir: str | Path, sweep_name: str) -> Path:
    """Create a timestamped sweep directory with a ``packets`` subdirectory."""

    safe_name = "".join(char if char.isalnum() or char in "-_" else "-" for char in sweep_name).strip("-")
    if not safe_name:
        raise ValueError("sweep_name must contain at least one alphanumeric character")
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    sweep_dir = Path(base_dir) / f"{timestamp}-{safe_name}"
    counter = 1
    while sweep_dir.exists():
        sweep_dir = Path(base_dir) / f"{timestamp}-{safe_name}-{counter}"
        counter += 1
    (sweep_dir / "packets").mkdir(parents=True, exist_ok=False)
    return sweep_dir


def build_sweep_config(
    *,
    betas: Iterable[float],
    seeds: Iterable[int],
    lattice_shape: tuple[int, int, int, int],
    n_sweeps: int,
    thermalization: int,
    measure_every: int,
    step_size: float,
    use_local_action: bool = True,
    hot_start: bool = False,
    n_bootstrap: int = 100,
    mean_mode: str = "global",
) -> dict[str, Any]:
    """Build a serializable beta/seed sweep configuration."""

    beta_values = [float(beta) for beta in betas]
    seed_values = [int(seed) for seed in seeds]
    if not beta_values:
        raise ValueError("betas must not be empty")
    if not seed_values:
        raise ValueError("seeds must not be empty")
    if int(measure_every) <= 0:
        raise ValueError("measure_every must be positive")
    if int(n_sweeps) <= int(thermalization):
        raise ValueError("n_sweeps must exceed thermalization")
    if float(step_size) <= 0.0:
        raise ValueError("step_size must be positive")
    if int(n_bootstrap) <= 0:
        raise ValueError("n_bootstrap must be positive")

    return {
        "label": "tiny finite-lattice beta/seed correlator packet sweep",
        "research_objective": DEFAULT_RESEARCH_OBJECTIVE,
        "claim_boundary": DEFAULT_CLAIM_BOUNDARY,
        "betas": beta_values,
        "seeds": seed_values,
        "lattice_shape": tuple(lattice_shape),
        "n_sweeps": int(n_sweeps),
        "thermalization": int(thermalization),
        "measure_every": int(measure_every),
        "step_size": float(step_size),
        "use_local_action": bool(use_local_action),
        "hot_start": bool(hot_start),
        "n_bootstrap": int(n_bootstrap),
        "mean_mode": str(mean_mode),
        "baseline": "standard SU(2) Wilson action only",
    }


def collect_correlator_chain(config: dict[str, Any], *, beta: float, seed: int) -> tuple[list[dict[str, float]], np.ndarray]:
    """Run one tiny local-action baseline chain and collect records/samples."""

    if not config.get("use_local_action", True):
        raise ValueError("sweep packet helper currently expects use_local_action=True")
    rng = np.random.default_rng(seed)
    lattice = Lattice4D(tuple(config["lattice_shape"]))
    field = GaugeField.random(lattice, rng) if config.get("hot_start", False) else GaugeField.cold(lattice)
    records: list[dict[str, float]] = []
    samples: list[np.ndarray] = []
    for sweep in range(1, int(config["n_sweeps"]) + 1):
        stats = metropolis_sweep_local(field, beta, step_size=float(config["step_size"]), rng=rng)
        if sweep > int(config["thermalization"]) and (sweep - int(config["thermalization"])) % int(config["measure_every"]) == 0:
            records.append(
                {
                    "sweep": float(sweep),
                    "action": wilson_action(field, beta),
                    "average_plaquette": average_plaquette(field),
                    "average_closure_defect": average_closure_defect(field),
                    "acceptance_rate": stats.acceptance_rate,
                }
            )
            samples.append(glueball_timeseries(field))
    if not records:
        raise ValueError("chain produced no measurements")
    return records, np.vstack(samples)


def make_sweep_summary_record(beta: float, seed: int, packet_dir: str | Path, packet_summary: dict[str, Any]) -> dict[str, Any]:
    """Build one CSV-safe sweep summary row."""

    return {
        "beta": float(beta),
        "seed": int(seed),
        "packet_dir": str(packet_dir),
        "mean_acceptance_rate": packet_summary.get("mean_acceptance_rate", ""),
        "final_average_plaquette": packet_summary.get("final_average_plaquette", ""),
        "final_average_closure_defect": packet_summary.get("final_average_closure_defect", ""),
        "n_measurements": packet_summary.get("n_measurements", ""),
        "research_objective": packet_summary.get("research_objective", DEFAULT_RESEARCH_OBJECTIVE),
        "claim_boundary": packet_summary.get("claim_boundary", DEFAULT_CLAIM_BOUNDARY),
    }


def run_beta_seed_sweep(sweep_dir: str | Path, config: dict[str, Any]) -> dict[str, Any]:
    """Run a beta/seed sweep and write sweep-level artifacts."""

    root = Path(sweep_dir)
    packets_dir = root / "packets"
    packets_dir.mkdir(parents=True, exist_ok=True)
    if not config.get("betas"):
        raise ValueError("config betas must not be empty")
    if not config.get("seeds"):
        raise ValueError("config seeds must not be empty")
    save_config_json(root / "sweep_config.json", config)

    packet_dirs: list[Path] = []
    for beta in config["betas"]:
        for seed in config["seeds"]:
            packet_config = {
                "label": f"tiny finite-lattice correlator diagnostic beta={beta} seed={seed}",
                "research_objective": config["research_objective"],
                "claim_boundary": config["claim_boundary"],
                "lattice_shape": tuple(config["lattice_shape"]),
                "beta": float(beta),
                "n_sweeps": int(config["n_sweeps"]),
                "step_size": float(config["step_size"]),
                "thermalization": int(config["thermalization"]),
                "measure_every": int(config["measure_every"]),
                "hot_start": bool(config["hot_start"]),
                "use_local_action": bool(config["use_local_action"]),
                "seed": int(seed),
                "n_bootstrap": int(config["n_bootstrap"]),
                "mean_mode": str(config["mean_mode"]),
                "baseline": config["baseline"],
            }
            records, samples = collect_correlator_chain(config, beta=float(beta), seed=int(seed))
            packet_name = f"beta_{float(beta):.1f}_seed_{int(seed)}".replace(".", "p")
            packet_dir = packets_dir / packet_name
            write_correlator_packet(
                packet_dir,
                packet_config,
                records,
                samples,
                n_bootstrap=int(config["n_bootstrap"]),
                seed=int(seed) + 1,
                mean_mode=str(config["mean_mode"]),
            )
            packet_dirs.append(packet_dir)

    comparisons = compare_packet_summaries(packet_dirs)
    sweep_rows = [
        make_sweep_summary_record(float(summary["beta"]), int(config["seeds"][index % len(config["seeds"])]), packet_dirs[index], summary)
        for index, summary in enumerate(comparisons)
    ]
    save_records_csv(root / "sweep_summary.csv", sweep_rows)
    save_packet_comparison_csv(root / "packet_comparison.csv", comparisons)
    save_manifest_json(
        root,
        {
            "packet_type": "beta_seed_sweep_diagnostic",
            "research_objective": config["research_objective"],
            "claim_boundary": config["claim_boundary"],
            "artifacts": {
                "sweep_config": "sweep_config.json",
                "sweep_summary": "sweep_summary.csv",
                "packet_comparison": "packet_comparison.csv",
                "packets": "packets/",
            },
            "n_packets": len(packet_dirs),
        },
    )
    return {
        "sweep_dir": str(root),
        "packet_dirs": [str(path) for path in packet_dirs],
        "summaries": comparisons,
    }
