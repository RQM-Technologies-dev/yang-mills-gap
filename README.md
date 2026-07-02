# yang-mills-gap

This repo is a disciplined conjecture program. Its central thesis is the
**Curvature-Closure Conjecture for the Yang-Mills Mass Gap**.

The project keeps a standard SU(2) Wilson-action lattice baseline auditable,
organizes finite-lattice diagnostics around a conjectural curvature-closure
mechanism, and makes the theorem-level obligations explicit.

## Direction

```text
standard SU(2) Wilson-action baseline
  -> auditable finite-lattice diagnostics
  -> conjectural curvature-closure mechanism
  -> Hamiltonian-gap-independent closure-energy definition
  -> vacuum isolation in gauge-invariant closure topology
  -> closure energy controls reconstructed Hamiltonian energy
  -> Yang-Mills mass-gap theorem, if the obligations are met
```

## Diagnostic Scope

The code currently supports:

- scalar-first unit-quaternion SU(2) link variables,
- plaquette holonomy and closure defect `D_p = 1 - scalar_part(U_p)`,
- Wilson action `S = beta * sum_p D_p`,
- full-action and local-action Metropolis checks,
- gauge-invariant plaquette and Wilson-loop observables,
- connected correlators and log/cosh effective-mass diagnostics,
- diagnostic packets, beta/seed sweeps, quality gates, and candidate
  assessments.

Finite-lattice packets serve as diagnostics for auditing the conjectural
mechanism. Packets, plots, effective-mass plateaus, and candidate assessments
help identify continuum spectral targets for theorem-level work.

## Conjecture Standards

Theorem-level development requires:

- a rigorous four-dimensional quantum Yang-Mills construction,
- continuum and infinite-volume control,
- a physical Hilbert-space construction,
- a theorem-level closure-coercivity result,
- a theorem showing that closure energy controls Hamiltonian energy,
- and a Clay Yang-Mills mass-gap theorem statement derived from those
  obligations.

The standard SU(2) Wilson-action baseline is the reference baseline for
diagnostics. Nonstandard anchor deformations belong to a separate interpretation
layer.

## Read Next

- `CLAIM_DISCIPLINE.md` - affirmative conjecture framing standards.
- `ROADMAP.md` - conjecture-oriented development sequence.
- `docs/07_proof_roadmap.md` - conjecture gap register.
- `docs/09_curvature_closure_proof.md` - curvature-closure conjecture thesis.
- `docs/10_closure_coercivity_lemma.md` - closure-coercivity target.
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
