# Roadmap

This roadmap is conjecture-oriented. Every phase supports the
**Curvature-Closure Conjecture for the Yang-Mills Mass Gap** while preserving
the standard SU(2) Wilson-action diagnostic baseline.

## 1. Standard SU(2) Wilson Baseline

- Maintain scalar-first unit-quaternion SU(2) links.
- Maintain plaquette holonomy, closure defect, and Wilson action.
- Maintain full-action and local-action Metropolis checks.
- Keep sweep packets tied to the explicit standard Wilson-action baseline
  contract.
- Verify unit norm, gauge invariance, Wilson-loop invariance, nonnegative
  action, and local action differences.

## 2. Numerical Quality

- Treat all finite-lattice outputs as diagnostics, not theorem evidence.
- Require packet configs, observables, diagnostics, plots, quality gates, and
  candidate assessments for spectroscopy comparisons.
- Track thermalization, autocorrelation, bootstrap/jackknife uncertainty, and
  effective-mass estimator health.
- Compare beta, seed, volume, operator choice, and local/full update sanity
  checks before increasing interpretive weight.

## 3. Gauge-Invariant Correlator Diagnostics

- Improve closed gauge-invariant operator bases built from plaquettes and
  spatial Wilson loops.
- Improve connected correlator statistics.
- Fit effective-mass plateaus only with uncertainty and packet diagnostics
  beside them.
- Use plateau and candidate reports only as finite-lattice signals that may
  suggest continuum spectral targets.

## 4. Closure-Energy Definitions

- Formulate curvature closure without changing the Wilson baseline.
- Define a non-circular closure-energy target independent of the Hamiltonian
  spectral gap.
- Specify admissible gauge-invariant curvature observables and the closure
  topology they generate.
- Track the renormalization needed to compare lattice Wilson closure cost to a
  continuum closure-energy quantity.

## 5. Closure-Coercivity Target

- State the future theorem obligation: the vacuum closure class would need to be
  isolated from the first nontrivial gauge-invariant curvature-closure class.
- Express the target as a positive lower bound for non-vacuum closure energy.
- Keep `docs/10_closure_coercivity_lemma.md` as the current lower-level
  non-circular conjectural target.

## 6. Closure-To-Hamiltonian Comparison

- Treat the Euclidean Yang-Mills measure and Osterwalder-Schrader
  reconstruction as future construction obligations, not repo-local results.
- Compare closure energy to reconstructed Hamiltonian energy only after the
  relevant objects are defined.
- Formulate the needed theorem: positive closure energy would force a positive
  lower Hamiltonian bound for every physical non-vacuum state.

## 7. Spectral-Gap Theorem Target

- Use the spectral theorem only as the final target after the construction,
  closure-coercivity, and Hamiltonian-comparison obligations are met.
- Treat exponential clustering either as a consequence of a gap or as a
  separately established equivalent route, not as an unproved input.
- Keep `docs/07_proof_roadmap.md` and
  `docs/09_curvature_closure_proof.md` aligned with this conjecture-first
  sequence.
