"""Utilities for writing reproducible diagnostic run packets."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping


def save_config_json(path: str | Path, config: Mapping[str, Any]) -> Path:
    """Write a JSON configuration file and return its path."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(dict(config), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_path


def save_records_csv(path: str | Path, records: Iterable[Mapping[str, Any]]) -> Path:
    """Write a sequence of flat record dictionaries to CSV."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [dict(record) for record in records]
    if not rows:
        raise ValueError("records must not be empty")

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


def save_diagnostics_json(path: str | Path, diagnostics: Mapping[str, Any]) -> Path:
    """Write diagnostic summaries as JSON and return the path."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(dict(diagnostics), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_path


def save_figure(run_dir: str | Path, figure, filename: str, *, dpi: int = 160) -> Path:
    """Save a Matplotlib figure under ``run_dir / "plots"``."""

    if Path(filename).name != filename:
        raise ValueError("filename must not include directory components")
    plots_dir = Path(run_dir) / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)
    output_path = plots_dir / filename
    figure.savefig(output_path, dpi=dpi)
    return output_path


def create_run_dir(base_dir: str | Path, run_name: str, config: Mapping[str, Any]) -> Path:
    """Create a timestamped run directory and immediately write ``config.json``."""

    safe_name = "".join(char if char.isalnum() or char in "-_" else "-" for char in run_name).strip("-")
    if not safe_name:
        raise ValueError("run_name must contain at least one alphanumeric character")

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = Path(base_dir) / f"{timestamp}-{safe_name}"
    counter = 1
    while run_dir.exists():
        run_dir = Path(base_dir) / f"{timestamp}-{safe_name}-{counter}"
        counter += 1

    (run_dir / "plots").mkdir(parents=True, exist_ok=False)
    save_config_json(run_dir / "config.json", config)
    return run_dir
