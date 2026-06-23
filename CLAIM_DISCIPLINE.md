# Claim Discipline

This repository is exploratory. It must be rigorous about what has and has not been shown.

## Allowed Claims

- The code implements a standard SU(2) Wilson lattice Yang-Mills baseline using unit-quaternion coordinates.
- Unit quaternions provide a concrete coordinate representation of SU(2) link variables.
- The plaquette scalar part is gauge invariant under local SU(2) gauge transformations.
- Closure defect `D_p = 1 - scalar_part(U_p)` is a useful local curvature proxy in the lattice representation.
- The included experiments generate toy numerical diagnostics on very small lattices.
- RQM language can be used as an interpretive hypothesis when clearly separated from the baseline action.

## Disallowed Claims

- Do not claim this repository proves the Yang-Mills mass gap.
- Do not claim a toy effective-mass plot establishes the Clay Millennium result.
- Do not claim RQM anchor deformations are standard Yang-Mills theory.
- Do not claim numerical evidence on finite lattices is a continuum proof.
- Do not blur the difference between interpretation, deformation, and theorem.

## Required Framing

Use this thesis as a hypothesis, not a theorem:

> "The Yang–Mills mass gap may be interpreted in RQM as the lowest nonzero energy of a closed, gauge-invariant non-abelian curvature resonance."

Recommended language:

- "This suggests an interpretive bridge..."
- "In the baseline Wilson-action model..."
- "This toy deformation explores..."
- "A proof would require..."

Avoid:

- "This proves..."
- "We solve..."
- "The mass gap follows immediately..."
- "The anchor term is Yang-Mills..."

## Baseline Versus Deformed Work

Baseline files under `src/rqm_yang_mills/` implement standard Wilson-action lattice Yang-Mills in quaternion coordinates.

Any nonstandard RQM anchor or closure deformation must be:

- implemented outside the baseline package or behind an unmistakable name,
- marked as nonstandard in script and plot titles,
- reported separately from baseline measurements,
- excluded from any claim about standard Yang-Mills unless a separate derivation is supplied.
