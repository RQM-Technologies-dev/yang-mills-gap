# Roadmap

## Phase 1: Standard SU(2) Lattice Baseline

- Implement NumPy unit-quaternion utilities.
- Build a periodic 4D lattice helper.
- Store SU(2) gauge fields as unit-quaternion link variables.
- Compute plaquette holonomy, closure defect, and Wilson action.
- Add gauge-invariant observables and simple Metropolis updates.
- Verify quaternion identities, plaquette identity behavior, gauge invariance, and nonnegative Wilson action.

## Phase 2: Baseline Numerical Quality

- Replace full-action Metropolis proposals with local staple action differences.
- Add autocorrelation estimates and thermalization diagnostics.
- Add bootstrap or jackknife errors for correlators.
- Explore beta and lattice-size dependence.

## Phase 3: Glueball-Like Correlators

- Refine spatial plaquette operators.
- Improve connected correlator statistics.
- Fit effective-mass plateaus with uncertainty estimates.
- Compare finite-volume and finite-spacing behavior.

## Phase 4: RQM Interpretation Layer

- Map plaquette holonomy to curvature closure.
- Map Wilson action to closure cost.
- Interpret the mass-gap target as the lowest nonzero closed gauge-invariant curvature resonance.
- Keep the interpretation separate from deformed dynamics.

## Phase 5: Nonstandard Anchor Deformations

- Explore anchor terms only in explicitly labeled nonstandard experiments.
- Compare deformed dynamics against the baseline without merging claims.
- Treat these experiments as hypothesis generators, not theorem evidence.

## Phase 6: Proof Roadmap

- Document what would be required for a continuum construction.
- Track the gaps between finite-lattice numerics and rigorous spectral claims.
- Keep proof-oriented language conditional until each analytical step is supplied.
