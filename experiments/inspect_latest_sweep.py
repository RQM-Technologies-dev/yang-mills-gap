"""Inspect the newest beta/seed diagnostic sweep under outputs/run_packets/sweeps."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def load_csv_rows(path: str | Path) -> list[dict[str, str]]:
    """Read a CSV file into dictionaries."""

    with Path(path).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def find_latest_sweep(base_dir: str | Path) -> Path:
    """Return the newest sweep directory containing sweep comparison artifacts."""

    root = Path(base_dir)
    candidates = [
        path
        for path in root.iterdir()
        if path.is_dir() and ((path / "packet_comparison.csv").exists() or (path / "sweep_summary.csv").exists())
    ]
    if not candidates:
        raise FileNotFoundError(f"no sweep directories found under {root}")
    return max(candidates, key=lambda path: path.stat().st_mtime)


def unique_values(rows: list[dict[str, str]], key: str) -> list[str]:
    """Return unique nonempty values in first-seen order."""

    values: list[str] = []
    for row in rows:
        value = row.get(key, "")
        if value and value not in values:
            values.append(value)
    return values


def finite_float(value: str | None) -> float | None:
    if value in {"", None}:
        return None
    try:
        number = float(value)
    except ValueError:
        return None
    return number if number == number and abs(number) != float("inf") else None


def best_packet_by_cosh_plateau(rows: list[dict[str, str]]) -> dict[str, str] | None:
    """Return the row with the lowest finite cosh plateau relative std."""

    finite_rows = [
        (finite_float(row.get("best_cosh_plateau_relative_std")), row)
        for row in rows
    ]
    candidates = [(value, row) for value, row in finite_rows if value is not None]
    if not candidates:
        return None
    return min(candidates, key=lambda item: item[0])[1]


def has_plateau_candidates(rows: list[dict[str, str]]) -> bool:
    """Return whether any packet reports log or cosh plateau candidates."""

    for row in rows:
        log_count = finite_float(row.get("n_log_plateau_candidates"))
        cosh_count = finite_float(row.get("n_cosh_plateau_candidates"))
        if (log_count is not None and log_count > 0) or (cosh_count is not None and cosh_count > 0):
            return True
    return False


def main() -> None:
    sweep_dir = find_latest_sweep(ROOT / "outputs" / "run_packets" / "sweeps")
    sweep_rows = load_csv_rows(sweep_dir / "sweep_summary.csv")
    comparison_rows = load_csv_rows(sweep_dir / "packet_comparison.csv")
    beta_values = unique_values(sweep_rows or comparison_rows, "beta")
    seed_values = unique_values(sweep_rows, "seed")
    best = best_packet_by_cosh_plateau(comparison_rows)

    print(f"Sweep directory: {sweep_dir}")
    print(f"Packets: {len(comparison_rows)}")
    print(f"Beta values: {', '.join(beta_values) if beta_values else '(none found)'}")
    if seed_values:
        print(f"Seed values: {', '.join(seed_values)}")

    if best is None:
        print("Best cosh plateau packet: unavailable")
    else:
        print("Best cosh plateau packet:")
        print(f"  run_dir: {best.get('run_dir', '')}")
        print(f"  beta: {best.get('beta', '')}")
        print(f"  best_cosh_plateau_mean: {best.get('best_cosh_plateau_mean', '')}")
        print(f"  best_cosh_plateau_relative_std: {best.get('best_cosh_plateau_relative_std', '')}")

    if not has_plateau_candidates(comparison_rows):
        print("WARNING: no plateau candidates found in packet_comparison.csv")


if __name__ == "__main__":
    main()
