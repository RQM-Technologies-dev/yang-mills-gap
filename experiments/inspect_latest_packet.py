"""Inspect the newest diagnostic packet or sweep under outputs/run_packets."""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from pprint import pprint

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from yang_mills_gap.packet_analysis import summarize_packet


def find_latest_packet(base_dir: str | Path) -> Path:
    """Return the newest directory under ``base_dir`` containing ``config.json``."""

    root = Path(base_dir)
    candidates = [path.parent for path in root.rglob("config.json") if path.is_file()]
    if not candidates:
        raise FileNotFoundError(f"no packet config.json files found under {root}")
    return max(candidates, key=lambda path: path.stat().st_mtime)


def read_first_rows(path: Path, limit: int = 5) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = []
        for index, row in enumerate(csv.DictReader(handle)):
            if index >= limit:
                break
            rows.append(dict(row))
    return rows


def print_optional_table(path: Path) -> None:
    if path.exists():
        print(f"\n{path}:")
        pprint(read_first_rows(path))


def main() -> None:
    packet_dir = find_latest_packet(ROOT / "outputs" / "run_packets")
    print(f"Latest packet: {packet_dir}")
    pprint(summarize_packet(packet_dir))

    # If the packet is nested under a sweep root, show sweep-level tables too.
    for parent in [packet_dir, *packet_dir.parents]:
        if parent == ROOT.parent:
            break
        print_optional_table(parent / "packet_comparison.csv")
        print_optional_table(parent / "sweep_summary.csv")
        if parent.name == "run_packets":
            break


if __name__ == "__main__":
    main()
