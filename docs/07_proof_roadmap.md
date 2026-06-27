# Proof Roadmap

This repository is a computational sandbox, not a proof.

The current proof draft is `docs/09_curvature_closure_proof.md`. It records the
curvature-closure theorem target and the proof burden; it does not close the
gaps listed below.

The lower-level coercivity target is `docs/10_closure_coercivity_lemma.md`.
It decomposes the core lemma into non-circular definitions of closure energy,
vacuum isolation, and the comparison between closure energy and Hamiltonian
energy.

Finite-lattice experiments can organize implementation evidence, test
discipline, and sharpen the curvature-closure proof target. They do not by
themselves establish the continuum theorem.

## Current Role Of The Repository

The repository can currently support proof-facing work only by making the
standard SU(2) Wilson-action finite-lattice baseline auditable:

- packetized configurations, observables, diagnostics, correlators, and plots,
- quality gates for thermalization, autocorrelation, uncertainty, and finite
  effective-mass diagnostics,
- packet-level closure-resonance candidate assessments with explicit failure
  reasons,
- and claim-boundary checks that keep interpretation separate from standard
  Yang-Mills evidence.

These are prerequisites for disciplined research. They are not a substitute
for construction, spectral analysis, or a continuum limit.

## Gap Register

A proof-oriented program would need to close at least these gaps:

| Gap | Current repository status | Required future evidence |
| --- | --- | --- |
| Four-dimensional quantum Yang-Mills construction | Not supplied | A rigorous construction of the target continuum theory |
| Gauge-invariant observable definitions | Finite-lattice Wilson loops and plaquette operators only | Continuum-compatible gauge-invariant observables |
| Physical Hilbert space | Not supplied | Reflection positivity or another route to physical states |
| Spectral formulation | Effective-mass diagnostics only | Transfer-matrix or Hamiltonian spectral control |
| Positive lowest non-vacuum energy | Packet-level candidates only | Proof that the lowest non-vacuum gauge-invariant energy is strictly positive |
| Closure coercivity | Proof target only | Non-circular closure energy, vacuum isolation, and Hamiltonian comparison |
| Continuum limit | Not supplied | Controlled lattice-spacing limit |
| Infinite-volume limit | Not supplied | Controlled thermodynamic limit |

## Translation Target

If finite-lattice packets eventually show stable candidate behavior, the next
mathematical translation target is:

```text
packet-level closed gauge-invariant curvature-resonance candidate
  -> controlled family of gauge-invariant lattice states/observables
  -> continuum-compatible spectral statement
  -> strictly positive lowest non-vacuum gauge-invariant energy
```

Each arrow is a missing analytical obligation. A plot, plateau heuristic, or
packet-level candidate can motivate one of these arrows, but cannot replace it.

## Non-Evidence

The following should not be treated as proof evidence:

- a finite effective-mass value from one packet,
- a plateau candidate without uncertainty, autocorrelation, and seed checks,
- a beta/seed trend without volume and lattice-spacing controls,
- an anchor-deformed run,
- or an interpretation statement without a corresponding standard Yang-Mills
  object.

## Advancement Standard

The project should move from numerical-roadmap language toward proof-roadmap
language only when the finite-lattice side has:

- unchanged standard Wilson-action dynamics,
- reproducible packet artifacts,
- quality gates reported and passing or explicitly explained,
- stable candidate assessments across beta, seed, operator, and volume checks,
- uncertainty-backed plateau fits,
- and a written translation target that names the exact continuum statement
  being approached.
