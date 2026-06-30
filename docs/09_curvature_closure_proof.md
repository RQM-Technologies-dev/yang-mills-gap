# Curvature-Closure Conjecture for the Yang-Mills Mass Gap

## Status

This document records the central conjectural mechanism for the repository and
the proof obligations that would be required to make it a theorem.

It is a conjecture thesis and research program, not a completed Clay Yang-Mills
existence and mass-gap proof.

The core mathematical burden is the closure-coercivity target: no sequence of
non-vacuum gauge-invariant curvature states should be able to approach the
vacuum with energy tending to zero.

That target is close to the mass-gap statement, so it cannot be assumed. The
required refinement is a lower-level structural statement: the vacuum closure
class would need to be isolated from the first nontrivial gauge-invariant
curvature-closure class, and the corresponding closure energy would need to
control Hamiltonian energy after reconstruction. See
`docs/10_closure_coercivity_lemma.md`.

## Main Conjecture

The **Curvature-Closure Conjecture for the Yang-Mills Mass Gap** says:

Classical Yang-Mills admits massless non-abelian gauge waves.
Pure quantum Yang-Mills admits only gauge-invariant physical states.
The physical non-vacuum states should be closed curvature resonances.
The lowest nonzero closed curvature resonance should have strictly positive
energy.
If those statements are made rigorous in the reconstructed standard Yang-Mills
theory, pure quantum Yang-Mills would have a mass gap.

## Target Theorem If Proved

Let `G` be a compact simple gauge group. The target theorem would assert the
existence of a nontrivial four-dimensional quantum Yang-Mills theory on `R^4`
whose local quantum fields correspond to gauge-invariant local polynomials in
the curvature `F` and its covariant derivatives.

The reconstructed physical Hilbert space `H_phys` would contain a unique
Poincare-invariant vacuum vector `Omega`, and its Hamiltonian `H` would satisfy

```text
Spec(H | H_phys) = {0} union [Delta, infinity)
```

for some finite `Delta > 0`.

Equivalently, for every physical state `psi in H_phys` with `psi` orthogonal to
`Omega`,

```text
<psi, H psi> >= Delta ||psi||^2.
```

This theorem is not established in this repository.

## Interpretation Layer

The conjectural interpretation is that the mass gap `Delta` is the minimum
energy required for nonzero Yang-Mills curvature to close into a stable
gauge-invariant resonance.

Open gauge-field propagation is the classical massless mode.
Closed gauge-invariant curvature resonance is the candidate quantum massive
excitation.
The mass gap would be the first nonzero closure energy if the conjecture is
made rigorous.

## Proof Obligations

Turning the conjecture into a theorem would require at least the following:

1. Construct the Euclidean Yang-Mills measure as the continuum limit of Wilson
   lattice gauge theory.

2. Establish reflection positivity, Euclidean invariance, locality, gauge
   invariance, nontriviality, and asymptotic-freedom-compatible short-distance
   behavior.

3. Use Osterwalder-Schrader reconstruction to obtain the physical Hilbert space,
   vacuum, Hamiltonian, momentum operators, and gauge-invariant local quantum
   fields.

4. Define a gauge-invariant curvature-closure functional independently of the
   Hamiltonian spectral gap. On the lattice this begins as Wilson closure cost;
   in the continuum target it must become a renormalized gauge-invariant
   closure energy for curvature-state classes.

5. Establish vacuum isolation in the gauge-invariant curvature-closure topology:

   The vacuum closure class would need to be separated from the first
   nontrivial physical closure class by a strictly positive closure threshold.

6. Establish the closure-coercivity target:

   Every non-vacuum gauge-invariant curvature state would need closure energy
   bounded below by a universal positive constant.

7. Establish that closure coercivity controls Hamiltonian energy after
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

## Core Target

No sequence of non-vacuum gauge-invariant curvature states should be able to
approach the vacuum with energy tending to zero.

In physical language: a nontrivial closed curvature resonance should not be
arbitrarily soft.

In the interpretation layer: closure should have a first nonzero resonance
threshold.

## Claim Boundary

The architecture is useful because it isolates the missing step. The
coercivity target cannot be assumed as a definition of mass gap; it would need
to be derived from the constructed Yang-Mills measure, reflection positivity,
the gauge-invariant observable algebra, and the reconstructed Hamiltonian.

The non-circular version requires three intermediate statements:

1. curvature closure energy is defined without reference to the Hamiltonian gap,
2. the vacuum is isolated in that closure-energy topology,
3. closure energy gives a lower bound for reconstructed Hamiltonian energy.

Equivalently, one must establish:

```text
Spec(H | H_phys) intersect (0, Delta) = empty
```

for some `Delta > 0`, rather than infer it from a finite-lattice effective-mass
plot or from terminology alone.

## Finite-Lattice Bridge

The repository's current SU(2) Wilson-action lattice diagnostics can support
this conjecture program by testing whether gauge-invariant curvature operators
show auditable finite-lattice signatures compatible with a first nonzero
resonance.

The finite-lattice bridge is:

```text
plaquette holonomy
  -> curvature closure diagnostic
  -> connected gauge-invariant correlator
  -> finite-lattice effective-mass candidate
  -> proposed continuum spectral target
```

This bridge organizes diagnostics and candidate definitions. It does not by
itself prove the continuum theorem.
