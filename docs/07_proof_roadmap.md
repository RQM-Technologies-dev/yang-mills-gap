# Conjecture Roadmap And Gap Register

This repository is a computational sandbox and conjecture-auditing environment,
not a proof of the Clay Yang-Mills problem.

The central thesis is the
**Curvature-Closure Conjecture for the Yang-Mills Mass Gap**, recorded in
`docs/09_curvature_closure_proof.md`. That document states a
conjectural mechanism and the obligations that would be needed to turn it into a
theorem.

The lower-level coercivity target is `docs/10_closure_coercivity_lemma.md`.
It decomposes the central obligation into non-circular definitions of closure
energy, vacuum isolation, and the comparison between closure energy and
Hamiltonian energy.

Finite-lattice experiments can organize diagnostics, test discipline, and
sharpen the conjecture. They do not by themselves establish the continuum
theorem.

## Current Role Of The Repository

The repository can currently support conjecture-auditing work by making the
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

A theorem-level development of the conjecture would need to close at least
these gaps:

| Gap | Current repository status | Required future evidence |
| --- | --- | --- |
| Four-dimensional quantum Yang-Mills construction | Not supplied | A rigorous construction of the target continuum theory |
| Gauge-invariant observable definitions | Finite-lattice Wilson loops and plaquette operators only | Continuum-compatible gauge-invariant observables |
| Physical Hilbert space | Not supplied | Reflection positivity or another route to physical states |
| Spectral formulation | Effective-mass diagnostics only | Transfer-matrix or Hamiltonian spectral control |
| Positive lowest non-vacuum energy | Packet-level candidates only | Theorem showing that the lowest non-vacuum gauge-invariant energy is strictly positive |
| Closure coercivity | Conjectural target only | Non-circular closure energy, vacuum isolation, and Hamiltonian comparison |
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

The following should not be treated as evidence that the standard Yang-Mills
mass-gap problem has been solved:

- a finite effective-mass value from one packet,
- a plateau candidate without uncertainty, autocorrelation, and seed checks,
- a beta/seed trend without volume and lattice-spacing controls,
- an anchor-deformed run,
- or an interpretation statement without a corresponding standard Yang-Mills
  object.

## Advancement Standard

The project should increase interpretive weight only when the finite-lattice
side has:

- unchanged standard Wilson-action dynamics,
- reproducible packet artifacts,
- quality gates reported and passing or explicitly explained,
- stable candidate assessments across beta, seed, operator, and volume checks,
- uncertainty-backed plateau fits,
- and a written translation target that names the exact continuum statement
  being approached.
