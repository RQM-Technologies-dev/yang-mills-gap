# Roadmap

## Phase 1: Standard SU(2) Baseline

- Implement scalar-first unit-quaternion SU(2) operations.
- Build a 4D periodic lattice and unit-quaternion link fields.
- Compute plaquettes, closure defects, Wilson action, and gauge-invariant observables.
- Add a clear but simple Metropolis update path.
- Validate quaternion identities, identity-field plaquettes, Wilson action consistency, and gauge invariance of plaquette scalar parts.

Status: implemented as the initial research scaffold.

## Phase 2: Numerical Baseline Quality

- Replace full-action Metropolis proposals with local staple-based action differences.
- Add autocorrelation estimates and thermalization diagnostics.
- Expand to larger lattices and ensembles.
- Add jackknife or bootstrap errors for correlators and effective masses.
- Separate connected and unconnected glueball operators in analysis scripts.

## Phase 3: Gauge-Invariant Resonance Diagnostics

- Study closure-defect distributions and spatial-plaquette operator spectra.
- Compare Wilson loops and glueball-like correlators across beta values and lattice sizes.
- Track whether candidate resonance language can be mapped to standard gauge-invariant observables without modifying the action.

## Phase 4: RQM Interpretation Layer

- Formalize the interpretive statement:

  > "The Yang–Mills mass gap may be interpreted in RQM as the lowest nonzero energy of a closed, gauge-invariant non-abelian curvature resonance."

- Keep this as an interpretation of standard gauge-invariant structures unless a script or document explicitly states otherwise.
- Identify which concepts correspond to standard lattice objects and which are new RQM vocabulary.

## Phase 5: Nonstandard Anchor Experiments

- Explore RQM-inspired anchor or closure deformations only in explicitly labeled scripts.
- Never mix deformed-action outputs with baseline Wilson-action claims.
- Treat deformations as hypothesis generators, not as proof evidence for the Clay problem.

## Phase 6: Proof Roadmap Work

- State what would be needed to connect lattice observations to continuum Yang-Mills theory.
- Track reflection positivity, transfer matrix, continuum limit, infinite-volume limit, gauge invariance, and operator definitions.
- Document gaps instead of smoothing them over.
