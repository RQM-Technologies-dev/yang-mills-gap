# yang-mills-gap

Python research sandbox for exploring a Resonant Quantum Mechanics interpretation of the Yang-Mills mass gap using standard SU(2) lattice Yang-Mills represented in unit-quaternion coordinates.

Central thesis:

> "The Yang-Mills mass gap may be interpreted in Resonant Quantum Mechanics as the lowest nonzero energy of a closed, gauge-invariant non-abelian curvature resonance."

This repository explores, models, interprets, and tests finite-lattice structures. It is not a Clay Yang-Mills mass-gap result.

## Research Objective

This repo is an attempt to build a disciplined Resonant Quantum Mechanics / Quaternionic Spectral Geometry route toward the Yang-Mills mass gap. The working hypothesis is that the Yang-Mills mass gap may arise as the lowest nonzero energy of a closed, gauge-invariant, non-abelian curvature resonance.

The research program separates standard SU(2) Wilson-action finite-lattice diagnostics, RQM/QSG interpretation, nonstandard deformation experiments, and the future continuum proof target. Finite-lattice packets are diagnostic evidence and engineering scaffolding, not a continuum proof by themselves.

For the closure-resonance interpretation roadmap, see `docs/08_closure_resonance_roadmap.md`.

## Scope

The first phase implements standard SU(2) Wilson lattice Yang-Mills without RQM deformation:

- SU(2) link variables are represented as scalar-first unit quaternions.
- Plaquette holonomy is used as the baseline curvature object.
- Closure defect is `D_p = 1 - scalar_part(U_p)`.
- Wilson action is interpreted as a standard closure cost: `S = beta * sum_p D_p`.
- Glueball-like spatial plaquette operators provide a finite-lattice route to connected correlators and effective-mass diagnostics.

RQM enters as an interpretation layer. Anchor deformation experiments are nonstandard and are separated from the baseline implementation.

## Numerical Status

The current experiments are tiny finite-lattice sanity diagnostics. They are meant to exercise the code paths and generate inspectable plots, not to produce meaningful mass-gap estimates.

Meaningful mass-gap estimates would require larger lattices, thermalization checks, autocorrelation estimates, uncertainty analysis, and systematic finite-volume and finite-spacing studies. The package now includes local staple-based action differences, a faster local Metropolis sweep, log and cosh effective-mass estimators, and bootstrap/jackknife correlator uncertainty helpers to support that later work.

Effective-mass plots from the current tiny runs should not be interpreted without thermalization, autocorrelation, and uncertainty diagnostics.

The anchor deformation example remains nonstandard and separate from the baseline Wilson action.

## Diagnostic Run Packets

The first reproducibility layer writes diagnostic run packets under `outputs/run_packets/`. A packet contains:

- `config.json` with the exact tiny-run configuration,
- `observables.csv` with measured Wilson-action observables,
- `diagnostics.json` with running means, autocorrelation, integrated autocorrelation time, and thermalization window summaries,
- `plots/` with diagnostic figures.

Use packets as the default container for future finite-lattice sanity diagnostics. No effective-mass plot should be interpreted without the accompanying diagnostics packet.

`exp_008_diagnostic_run_packet.py` writes observable diagnostics for action and average closure defect. `exp_009_correlator_run_packet.py` adds glueball-like samples, connected correlator diagnostics, bootstrap uncertainty, and log/cosh effective-mass diagnostics. Both are finite-lattice sanity diagnostics only, not Clay mass-gap results.

## Sweep Packets

`exp_010_beta_seed_sweep_packets.py` creates a tiny beta/seed sweep of correlator/effective-mass packets under `outputs/run_packets/sweeps/`. It writes per-packet artifacts plus `sweep_config.json`, `sweep_summary.csv`, `packet_comparison.csv`, and a sweep `manifest.json`.

`inspect_latest_sweep.py` summarizes the newest sweep, including beta/seed coverage and the best packet under a simple cosh effective-mass plateau heuristic.

`exp_011_larger_spectroscopy_sweep.py` runs a modest larger diagnostic sweep with a configurable lattice, beta list, seed list, sweep count, thermalization cut, measurement cadence, step size, and glueball-like operator. Its default operator averages gauge-invariant spatial 1x1, 1x2, and 2x1 Wilson loops. This is still a standard Wilson-action baseline measurement choice, not an anchor deformation.

Sweep packet comparisons are implementation diagnostics for the finite-lattice baseline. They are useful for auditing trends and failure modes, but they are not Yang-Mills mass-gap evidence at the continuum level. Plateau detection is a heuristic diagnostic for candidate flat windows; it is not a proof of a mass gap.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Run the small examples:

```bash
python experiments/exp_001_quaternion_su2_sanity.py
python experiments/exp_002_plaquette_closure_defect.py
python experiments/exp_003_wilson_action_metropolis.py
python experiments/exp_004_glueball_correlator.py
python experiments/exp_005_effective_mass_plateau.py
python experiments/exp_006_rqm_anchor_deformation_nonstandard.py
python experiments/exp_007_full_vs_local_metropolis_sanity.py
python experiments/exp_008_diagnostic_run_packet.py
python experiments/exp_009_correlator_run_packet.py
python experiments/exp_010_beta_seed_sweep_packets.py
python experiments/exp_011_larger_spectroscopy_sweep.py
python experiments/inspect_latest_sweep.py
```

Figures are written to `outputs/figures`. Numerical data is written to `outputs/data`.

## Package Layout

```text
src/yang_mills_gap/
  baseline_contract.py Contract helpers for standard Wilson-action diagnostics
  quaternions.py       NumPy unit-quaternion operations for SU(2)
  lattice.py           Periodic 4D lattice helper
  gauge_field.py       Unit-quaternion link field U[x, y, z, t, mu]
  plaquette.py         Plaquette holonomy and closure defect
  wilson_action.py     Standard Wilson action and local staple utilities
  observables.py       Average plaquette, closure defect, glueball-like operators
  monte_carlo.py       Full-action reference and local-action Metropolis sweeps
  correlators.py       Connected temporal correlator plus bootstrap/jackknife helpers
  effective_mass.py    Log and cosh effective-mass estimators
  plateau.py           Simple effective-mass plateau heuristics
  candidate.py         Packet-level closure-resonance candidate assessment
  diagnostics.py       Running means, autocorrelation, thermalization summaries
  quality_gates.py     Packet-level quality gates for diagnostic interpretation
  experiment_driver.py Shared tiny-chain diagnostic driver
  packet_analysis.py   Dependency-light packet loading and summaries
  packet_compare.py    Packet summary and comparison CSV helpers
  packet_plots.py      Reusable diagnostic plot helpers
  run_packet.py        Reproducible diagnostic packet writers
  spectroscopy_packet.py Correlator/effective-mass packet helpers
  sweep_packets.py     Beta/seed sweep packet helpers
```

Read `CLAIM_DISCIPLINE.md` before using this repository for public claims or summaries.
For proof-facing gaps, see `docs/07_proof_roadmap.md`.
For the current curvature-closure proof draft, see `docs/09_curvature_closure_proof.md`.
