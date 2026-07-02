# Conjecture Roadmap And Gap Register

This repository is a computational sandbox and conjecture-auditing environment
for the Clay Yang-Mills mass-gap problem.

The central thesis is the
**Curvature-Closure Conjecture for the Yang-Mills Mass Gap**, recorded in
`docs/09_curvature_closure_proof.md`. That document states a conjectural
mechanism and the obligations that turn it into a theorem.

The lower-level coercivity target is `docs/10_closure_coercivity_lemma.md`.
It decomposes the central obligation into a closure-energy definition that is
independent of the Hamiltonian spectral gap, vacuum isolation, and the
comparison between closure energy and Hamiltonian energy.

Finite-lattice experiments organize diagnostics, test discipline, and sharpen
the conjecture.

## Current Role Of The Repository

The repository supports conjecture-auditing work by making the standard SU(2)
Wilson-action finite-lattice baseline auditable:

- packetized configurations, observables, diagnostics, correlators, and plots,
- quality gates for thermalization, autocorrelation, uncertainty, and finite
  effective-mass diagnostics,
- packet-level closure-resonance candidate assessments with explicit failure
  reasons,
- and claim-boundary checks that keep interpretation tied to standard
  Yang-Mills objects.

These are prerequisites for disciplined research and inputs to construction,
spectral analysis, and continuum-limit work.

## Gap Register

A theorem-level development of the conjecture requires progress on these gaps:

| Gap | Current repository status | Required future evidence |
| --- | --- | --- |
| Four-dimensional quantum Yang-Mills construction | Theorem obligation | A rigorous construction of the target continuum theory |
| Gauge-invariant observable definitions | Finite-lattice Wilson loops and plaquette operators | Continuum-compatible gauge-invariant observables |
| Physical Hilbert space | Theorem obligation | Reflection positivity or another route to physical states |
| Spectral formulation | Effective-mass diagnostics | Transfer-matrix or Hamiltonian spectral control |
| Positive lowest non-vacuum energy | Packet-level candidates | Theorem showing that the lowest non-vacuum gauge-invariant energy is strictly positive |
| Closure coercivity | Conjectural target | Hamiltonian-gap-independent closure energy, vacuum isolation, and Hamiltonian comparison |
| Continuum limit | Theorem obligation | Controlled lattice-spacing limit |
| Infinite-volume limit | Theorem obligation | Controlled thermodynamic limit |

## Translation Target

If finite-lattice packets eventually show stable candidate behavior, the next
mathematical translation target is:

```text
packet-level closed gauge-invariant curvature-resonance candidate
  -> controlled family of gauge-invariant lattice states/observables
  -> continuum-compatible spectral statement
  -> strictly positive lowest non-vacuum gauge-invariant energy
```

Each arrow is an analytical obligation. A plot, plateau heuristic, or
packet-level candidate can motivate one of these arrows as theorem-level work.

## Diagnostic Interpretation

Finite-lattice interpretation uses:

- finite effective-mass values as packet diagnostics,
- plateau candidates with uncertainty, autocorrelation, and seed checks,
- beta/seed trends with volume and lattice-spacing controls,
- standard SU(2) Wilson-action runs as the reference baseline,
- and interpretation statements paired with corresponding standard Yang-Mills
  objects.

## Advancement Standard

The project increases interpretive weight when the finite-lattice side has:

- unchanged standard Wilson-action dynamics,
- reproducible packet artifacts,
- quality gates reported and passing or explicitly explained,
- stable candidate assessments across beta, seed, operator, and volume checks,
- uncertainty-backed plateau fits,
- and a written translation target that names the exact continuum statement
  being approached.
