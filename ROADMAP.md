# Roadmap

## Phase 1: Standard SU(2) Lattice Baseline

- Implement NumPy unit-quaternion utilities.
- Build a periodic 4D lattice helper.
- Store SU(2) gauge fields as unit-quaternion link variables.
- Compute plaquette holonomy, closure defect, and Wilson action.
- Add gauge-invariant observables, full-action reference Metropolis updates, and local staple-based Metropolis updates.
- Verify quaternion identities, plaquette identity behavior, gauge invariance, Wilson-loop invariance, nonnegative Wilson action, and local action differences.

## Phase 2: Baseline Numerical Quality

- Treat current experiments as tiny finite-lattice sanity diagnostics.
- Add autocorrelation estimates and thermalization diagnostics before interpreting long chains.
- Use bootstrap or jackknife errors for correlators and effective-mass diagnostics.
- Compare full-action and local-action Metropolis paths on tiny lattices as an implementation sanity check.
- Wrap finite-lattice sanity runs in diagnostic packets with config, observables, diagnostics, and plots.
- Explore beta and lattice-size dependence.
- Move from smoke-test lattices to larger volumes only after baseline diagnostics are stable.

## Phase 3: Glueball-Like Correlators

- Refine spatial plaquette operators.
- Improve connected correlator statistics.
- Fit effective-mass plateaus with uncertainty estimates.
- Compare finite-volume and finite-spacing behavior.
- Require larger lattices, thermalization checks, autocorrelation estimates, and uncertainty analysis before treating an effective-mass plateau as physically meaningful.
- Treat effective-mass plots as diagnostics only until thermalization, autocorrelation, and uncertainty checks are reported beside them.
- Require an accompanying diagnostic packet before comparing effective-mass plots across runs.

## Phase 4: RQM Interpretation Layer

- Map plaquette holonomy to curvature closure.
- Map Wilson action to closure cost.
- Interpret the mass-gap target as the lowest nonzero closed gauge-invariant curvature resonance.
- Keep the interpretation separate from deformed dynamics.

## Phase 5: Nonstandard Anchor Deformations

- Explore anchor terms only in explicitly labeled nonstandard experiments.
- Compare deformed dynamics against the baseline without merging claims.
- Treat these experiments as hypothesis generators, not theorem evidence.
- Do not merge anchor terms into the baseline Wilson action.

## Phase 6: Proof Roadmap

- Document what would be required for a continuum construction.
- Track the gaps between finite-lattice numerics and rigorous spectral claims.
- Keep proof-oriented language conditional until each analytical step is supplied.
