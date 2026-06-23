"""Read and summarize diagnostic run packets."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import numpy as np


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _parse_scalar(value: str) -> Any:
    if value == "":
        return value
    try:
        if value.lower() in {"true", "false"}:
            return value.lower() == "true"
    except AttributeError:
        return value
    try:
        number = float(value)
    except ValueError:
        return value
    return int(number) if number.is_integer() else number


def load_config(run_dir: str | Path) -> dict[str, Any]:
    """Load ``config.json`` from a run packet."""

    return _load_json(Path(run_dir) / "config.json")


def load_observables(run_dir: str | Path) -> list[dict[str, Any]]:
    """Load ``observables.csv`` as a list of plain dictionaries."""

    path = Path(run_dir) / "observables.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        return [{key: _parse_scalar(value) for key, value in row.items()} for row in csv.DictReader(handle)]


def load_diagnostics(run_dir: str | Path) -> dict[str, Any]:
    """Load ``diagnostics.json`` from a run packet."""

    return _load_json(Path(run_dir) / "diagnostics.json")


def load_manifest(run_dir: str | Path) -> dict[str, Any]:
    """Load ``manifest.json`` if present, otherwise return an empty manifest."""

    path = Path(run_dir) / "manifest.json"
    return _load_json(path) if path.exists() else {}


def load_packet(run_dir: str | Path) -> dict[str, Any]:
    """Load standard packet files and manifest-listed NumPy arrays."""

    root = Path(run_dir)
    manifest = load_manifest(root)
    arrays: dict[str, np.ndarray] = {}
    for name, relative_path in manifest.get("arrays", {}).items():
        arrays[name] = np.load(root / relative_path)
    return {
        "run_dir": str(root),
        "config": load_config(root),
        "manifest": manifest,
        "observables": load_observables(root),
        "diagnostics": load_diagnostics(root),
        "arrays": arrays,
    }


def summarize_packet(run_dir: str | Path) -> dict[str, Any]:
    """Return a compact plain-dictionary packet summary."""

    packet = load_packet(run_dir)
    observables = packet["observables"]
    diagnostics = packet["diagnostics"]
    final_record = observables[-1] if observables else {}
    manifest = packet["manifest"]
    return {
        "run_dir": packet["run_dir"],
        "label": packet["config"].get("label"),
        "claim_boundary": packet["config"].get("claim_boundary"),
        "n_observations": len(observables),
        "final_record": final_record,
        "diagnostic_keys": sorted(key for key in diagnostics.keys()),
        "artifacts": manifest.get("artifacts", {}),
        "arrays": {key: list(value.shape) for key, value in packet["arrays"].items()},
    }
