# Claim Discipline

This is an exploratory research repository. It is not a Clay Yang-Mills mass-gap result.

## Use These Verbs

- explores
- models
- interprets
- tests
- compares
- suggests

## Avoid Overclaiming Language

- establishes the Clay result
- derives the continuum theorem
- settles the Millennium problem
- finishes the mathematical program

## Baseline Claim Boundary

The baseline implementation is standard SU(2) Wilson lattice Yang-Mills in unit-quaternion coordinates. It does not include an RQM anchor term, resonance constraint, or deformation.

Allowed baseline claims:

- Unit quaternions model SU(2) link variables.
- Plaquette holonomy models lattice curvature.
- `D_p = 1 - scalar_part(U_p)` is the local closure defect used in the Wilson action.
- `S = beta * sum_p D_p` is the implemented Wilson action.
- Plaquette scalar parts are invariant under local gauge transformations.
- The included experiments are small finite-lattice diagnostics.

## RQM Interpretation Boundary

The thesis:

> "The Yang-Mills mass gap may be interpreted in Resonant Quantum Mechanics as the lowest nonzero energy of a closed, gauge-invariant non-abelian curvature resonance."

is an interpretation hypothesis. In this repository:

- plaquette holonomy is interpreted as curvature closure,
- Wilson action is interpreted as closure cost,
- glueball-like correlators are used as gauge-invariant resonance diagnostics,
- effective mass is treated as a finite-lattice diagnostic, not a theorem.

## Nonstandard Deformation Boundary

RQM anchor deformation experiments are nonstandard. They must remain separate from the baseline Yang-Mills implementation and must be described as exploratory deformations.

Do not use anchor-deformed outputs as evidence for a standard Yang-Mills theorem.
