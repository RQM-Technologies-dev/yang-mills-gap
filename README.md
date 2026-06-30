# yang-mills-gap

This repo is a disciplined curvature-closure proof program for Yang-Mills
existence and positive spectral gap.

It is not a completed Clay proof. Its current role is to build a standard
SU(2) Wilson lattice baseline, organize finite-lattice diagnostics as proof
scaffolding, and keep the proof burden explicit.

## Direction

```text
standard SU(2) Wilson lattice baseline
  -> auditable finite-lattice diagnostics
  -> non-circular curvature-closure energy
  -> vacuum isolation in gauge-invariant closure topology
  -> closure energy controls reconstructed Hamiltonian energy
  -> positive spectral gap
```

## Current Baseline

The code currently supports:

- scalar-first unit-quaternion SU(2) link variables,
- plaquette holonomy and closure defect `D_p = 1 - scalar_part(U_p)`,
- Wilson action `S = beta * sum_p D_p`,
- full-action and local-action Metropolis checks,
- gauge-invariant plaquette and Wilson-loop observables,
- connected correlators and log/cosh effective-mass diagnostics,
- diagnostic packets, beta/seed sweeps, quality gates, and candidate
  assessments.

These are finite-lattice proof scaffolding only. Packets, plots, effective-mass
plateaus, and candidate assessments do not prove the continuum theorem.

## Not Claimed

This repo does not currently provide:

- a rigorous four-dimensional quantum Yang-Mills construction,
- a continuum or infinite-volume limit,
- a physical Hilbert-space construction,
- a proof of closure coercivity,
- a proof that closure energy controls Hamiltonian energy,
- or a completed Clay Yang-Mills mass-gap proof.

Nonstandard anchor deformations are not part of the proof route and must not be
used as evidence for standard Yang-Mills.

## Read Next

- `CLAIM_DISCIPLINE.md` - allowed and forbidden public claims.
- `ROADMAP.md` - proof-oriented development sequence.
- `docs/07_proof_roadmap.md` - proof-gap register.
- `docs/09_curvature_closure_proof.md` - current proof draft.
- `docs/10_closure_coercivity_lemma.md` - non-circular closure-coercivity target.
- `docs/references/yangmills.pdf` - Clay problem statement PDF.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Run baseline diagnostics:

```bash
python experiments/exp_001_quaternion_su2_sanity.py
python experiments/exp_002_plaquette_closure_defect.py
python experiments/exp_003_wilson_action_metropolis.py
python experiments/exp_004_glueball_correlator.py
python experiments/exp_005_effective_mass_plateau.py
python experiments/exp_007_full_vs_local_metropolis_sanity.py
python experiments/exp_008_diagnostic_run_packet.py
python experiments/exp_009_correlator_run_packet.py
python experiments/exp_010_beta_seed_sweep_packets.py
python experiments/exp_011_larger_spectroscopy_sweep.py
python experiments/inspect_latest_sweep.py
```

Figures are written to `outputs/figures`. Numerical data is written to
`outputs/data`.

## Package Layout

```text
src/yang_mills_gap/
  baseline_contract.py   Standard Wilson-action baseline contract
  quaternions.py         Unit-quaternion SU(2) utilities
  lattice.py             Periodic 4D lattice helper
  gauge_field.py         Unit-quaternion link field
  plaquette.py           Plaquette holonomy and closure defect
  wilson_action.py       Wilson action and local staple utilities
  observables.py         Gauge-invariant plaquette and Wilson-loop observables
  monte_carlo.py         Full-action and local-action Metropolis sweeps
  correlators.py         Connected temporal correlators
  effective_mass.py      Log and cosh effective-mass estimators
  plateau.py             Plateau heuristics for diagnostics
  candidate.py           Packet-level candidate assessment
  diagnostics.py         Finite-chain diagnostics
  quality_gates.py       Packet-level quality gates
  run_packet.py          Reproducible diagnostic packet writers
  spectroscopy_packet.py Correlator/effective-mass packet helpers
  sweep_packets.py       Beta/seed sweep packet helpers
```
