# yang-mills-gap

Exploratory research code for studying a Resonant Quantum Mechanics interpretation of the Yang-Mills mass gap through SU(2) lattice Yang-Mills represented by unit quaternions.

Central thesis:

> "The Yang–Mills mass gap may be interpreted in RQM as the lowest nonzero energy of a closed, gauge-invariant non-abelian curvature resonance."

This repository does not claim to solve the Clay Millennium Yang-Mills existence and mass gap problem. The first phase implements a standard SU(2) Wilson lattice Yang-Mills baseline in quaternionic coordinates. Later RQM-inspired closure or anchor experiments are marked as nonstandard and are kept outside the baseline implementation.

## What Is Implemented

- Scalar-first unit-quaternion utilities for SU(2): normalize, multiply, conjugate, inverse, random sampling, and scalar part.
- A 4D periodic lattice with coordinate order `(x, y, z, t)`.
- SU(2) gauge fields as unit-quaternion links `U[x, y, z, t, mu]`.
- Plaquettes:

  ```text
  U_mu(x) U_nu(x + mu) U_mu^-1(x + nu) U_nu^-1(x)
  ```

- Closure defect `D_p = 1 - scalar_part(U_p)`.
- Wilson action `S = beta * sum_p D_p`.
- Basic Metropolis updates that preserve unit norm.
- Gauge-invariant observables: average plaquette, Wilson loops, spatial-plaquette glueball-like operator, temporal correlators, and effective mass.
- Small reproducible experiments that save plots to `outputs/figures` and data to `outputs/data`.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Run experiments from the repo root:

```bash
python experiments/exp_001_su2_plaquette_sanity.py
python experiments/exp_002_wilson_action_metropolis.py
python experiments/exp_003_glueball_correlator.py
python experiments/exp_004_effective_mass_plateau.py
python experiments/exp_005_closure_defect_histograms.py
python experiments/exp_006_rqm_anchor_deformation.py
```

`exp_006_rqm_anchor_deformation.py` is intentionally nonstandard. It is a toy deformation experiment, not part of the baseline Yang-Mills action.

## Package Layout

```text
src/rqm_yang_mills/
  quaternions.py       Unit-quaternion SU(2) utilities
  lattice.py           4D periodic lattice
  gauge_field.py       Link-field container and gauge transforms
  plaquette.py         Plaquette scalars and closure defects
  wilson_action.py     Standard Wilson action
  observables.py       Average plaquette, Wilson loops, glueball-like O(t)
  monte_carlo.py       Small-lattice Metropolis updates
  correlators.py       Temporal correlators
  effective_mass.py    log(C(t) / C(t+1)) estimator
```

## Claim Boundary

This repo is for computation, hypothesis formation, and proof-roadmap discipline. A numerical mass scale, toy effective-mass plateau, or RQM-motivated deformation is not evidence of a mathematical proof. See `CLAIM_DISCIPLINE.md` before writing results, abstracts, or public claims from this code.
