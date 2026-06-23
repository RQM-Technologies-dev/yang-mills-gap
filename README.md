# yang-mills-gap

Python research sandbox for exploring a Resonant Quantum Mechanics interpretation of the Yang-Mills mass gap using standard SU(2) lattice Yang-Mills represented in unit-quaternion coordinates.

Central thesis:

> "The Yang-Mills mass gap may be interpreted in Resonant Quantum Mechanics as the lowest nonzero energy of a closed, gauge-invariant non-abelian curvature resonance."

This repository explores, models, interprets, and tests finite-lattice structures. It is not a Clay Yang-Mills mass-gap result.

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
```

Figures are written to `outputs/figures`. Numerical data is written to `outputs/data`.

## Package Layout

```text
src/yang_mills_gap/
  quaternions.py       NumPy unit-quaternion operations for SU(2)
  lattice.py           Periodic 4D lattice helper
  gauge_field.py       Unit-quaternion link field U[x, y, z, t, mu]
  plaquette.py         Plaquette holonomy and closure defect
  wilson_action.py     Standard Wilson action and local staple utilities
  observables.py       Average plaquette, closure defect, glueball-like O(t)
  monte_carlo.py       Full-action reference and local-action Metropolis sweeps
  correlators.py       Connected temporal correlator plus bootstrap/jackknife helpers
  effective_mass.py    Log and cosh effective-mass estimators
  diagnostics.py       Running means, autocorrelation, thermalization summaries
```

Read `CLAIM_DISCIPLINE.md` before using this repository for public claims or summaries.
