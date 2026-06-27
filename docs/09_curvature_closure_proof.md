# Curvature-Closure Construction Of Quantum Yang-Mills And The Positive Resonance Gap

## Status

This document records the proposed RQM/QSG proof thesis and proof architecture.
It is a proof draft and research program, not a completed Clay Yang-Mills
existence and mass-gap proof.

The core mathematical burden is the curvature-closure coercivity lemma: no
sequence of non-vacuum gauge-invariant curvature states can approach the vacuum
with energy tending to zero.

That lemma is close to the mass-gap statement. The next required refinement is
to prove a lower-level structural statement: the vacuum closure class is isolated
from the first nontrivial gauge-invariant curvature-closure class, and the
corresponding closure energy controls Hamiltonian energy after reconstruction.
See `docs/10_closure_coercivity_lemma.md`.

## Main Thesis

Classical Yang-Mills admits massless non-abelian gauge waves.
Pure quantum Yang-Mills admits only gauge-invariant physical states.
The physical non-vacuum states are closed curvature resonances.
The lowest nonzero closed curvature resonance has strictly positive energy.
Therefore pure quantum Yang-Mills has a mass gap.

## Main Theorem

Let `G` be a compact simple gauge group. There exists a nontrivial
four-dimensional quantum Yang-Mills theory on `R^4` whose local quantum fields
correspond to gauge-invariant local polynomials in the curvature `F` and its
covariant derivatives.

The reconstructed physical Hilbert space `H_phys` contains a unique
Poincare-invariant vacuum vector `Omega`, and its Hamiltonian `H` satisfies

```text
Spec(H | H_phys) = {0} union [Delta, infinity)
```

for some finite `Delta > 0`.

Equivalently, for every physical state `psi in H_phys` with `psi` orthogonal to
`Omega`,

```text
<psi, H psi> >= Delta ||psi||^2.
```

## RQM Interpretation

The mass gap `Delta` is the minimum energy required for nonzero Yang-Mills
curvature to close into a stable gauge-invariant resonance.

Open gauge-field propagation is the classical massless mode.
Closed gauge-invariant curvature resonance is the quantum massive excitation.
The mass gap is the first nonzero closure energy.

## Proof Architecture

1. Construct the Euclidean Yang-Mills measure as the continuum limit of Wilson
   lattice gauge theory.

2. Prove reflection positivity, Euclidean invariance, locality, gauge
   invariance, nontriviality, and asymptotic-freedom-compatible short-distance
   behavior.

3. Use Osterwalder-Schrader reconstruction to obtain the physical Hilbert space,
   vacuum, Hamiltonian, momentum operators, and gauge-invariant local quantum
   fields.

4. Define a gauge-invariant curvature-closure functional independently of the
   Hamiltonian spectral gap. On the lattice this begins as Wilson closure cost;
   in the continuum target it must become a renormalized gauge-invariant
   closure energy for curvature-state classes.

5. Prove vacuum isolation in the gauge-invariant curvature-closure topology:

   The vacuum closure class is separated from the first nontrivial physical
   closure class by a strictly positive closure threshold.

6. Prove the curvature-closure coercivity lemma:

   Every non-vacuum gauge-invariant curvature state has closure energy bounded
   below by a universal positive constant.

7. Prove that closure coercivity controls Hamiltonian energy after
   Osterwalder-Schrader reconstruction:

   ```text
   E_closure(psi) >= epsilon > 0
     -> <psi, H psi> >= Delta ||psi||^2
   ```

8. Conclude by the spectral theorem that the Hamiltonian has no physical
   spectrum in `(0, Delta)`.

9. Derive, or separately identify as an equivalent diagnostic under the needed
   hypotheses, exponential clustering for connected gauge-invariant curvature
   correlators:

   ```text
   |<Omega, O(x) O(y) Omega>_c| <= C_O exp(-Delta |x-y|)
   ```

   for all suitable gauge-invariant curvature operators `O`.

## Core Lemma

No sequence of non-vacuum gauge-invariant curvature states can approach the
vacuum with energy tending to zero.

In physical language: a nontrivial closed curvature resonance cannot be made
arbitrarily soft.

In RQM language: closure has a first nonzero resonance threshold.

## Proof Burden

The proof architecture is sharp because it isolates the missing step. The
coercivity lemma cannot be assumed as a definition of mass gap; it must be
derived from the constructed Yang-Mills measure, reflection positivity, the
gauge-invariant observable algebra, and the reconstructed Hamiltonian.

The non-circular version requires three intermediate statements:

1. curvature closure energy is defined without reference to the Hamiltonian gap,
2. the vacuum is isolated in that closure-energy topology,
3. closure energy gives a lower bound for reconstructed Hamiltonian energy.

Equivalently, one must prove:

```text
Spec(H | H_phys) intersect (0, Delta) = empty
```

for some `Delta > 0`, rather than infer it from a finite-lattice effective-mass
plot or from RQM terminology alone.

## Finite-Lattice Bridge

The repository's current SU(2) Wilson-action lattice diagnostics can support
this proof program by testing whether gauge-invariant curvature operators show
auditable finite-lattice signatures compatible with a first nonzero resonance.

The finite-lattice bridge is:

```text
plaquette holonomy
  -> curvature closure diagnostic
  -> connected gauge-invariant correlator
  -> finite-lattice effective-mass candidate
  -> proposed continuum spectral target
```

This bridge organizes evidence and definitions. It does not by itself prove the
continuum theorem.
