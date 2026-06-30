# Closure-Coercivity Target

## Status

This document records the main lower-level coercivity target for the
**Curvature-Closure Conjecture for the Yang-Mills Mass Gap** in
`docs/09_curvature_closure_proof.md`.

The target prevents circularity by defining closure energy independently,
establishing vacuum isolation in that closure structure, and then deriving a
Hamiltonian spectral lower bound.

Closure energy, vacuum isolation, and Hamiltonian control are future proof
obligations for the conjecture program.

## Target Statement

The conjectural coercivity statement is:

Nontrivial gauge-invariant curvature closure should require a minimum nonzero
renormalized action or energy because the vacuum closure class should be
isolated from the first nontrivial physical closure class.

In formula form, the desired target is:

```text
inf E_closure(C) >= epsilon > 0
```

where the infimum is over all non-vacuum gauge-invariant physical
curvature-closure classes `C`.

The desired consequence after Osterwalder-Schrader reconstruction is:

```text
<psi, H psi> >= Delta ||psi||^2
```

for every physical state `psi` orthogonal to the vacuum.

Both statements are theorem-level goals of the conjecture program.

## Required Non-Circular Definitions

The target needs three definitions made independently of the Hamiltonian gap.

1. **Gauge-invariant curvature state.**
   A state generated from the vacuum by gauge-invariant smeared local
   polynomials in curvature and covariant derivatives, such as schematic
   observables of the form:

   ```text
   O_f(A) = integral f(x) P(F_A, D_A F_A, ...) dx
   ```

   with vacuum expectation removed when needed.

2. **Closure topology.**
   A topology on gauge-equivalence classes generated only by gauge-invariant
   curvature observables. Two configurations are close only if all admissible
   smeared curvature-closure probes agree within the chosen tolerances.

3. **Renormalized closure energy.**
   A continuum-limit version of lattice Wilson closure cost, defined before any
   appeal to a Hamiltonian gap. The lattice model starts from:

   ```text
   S_W[U] = beta(a) sum_p (1 - scalar_part(U_p))
   ```

   A candidate continuum target has the schematic form:

   ```text
   E_closure(C)
     = liminf_{a -> 0, L -> infinity}
       inf_{U in C_{a,L}}
       Z_cl(a,L) (S_W[U] - S_W[vacuum])
   ```

   where `C_{a,L}` is a lattice representative of the gauge-invariant closure
   class, and `Z_cl(a,L)` is the renormalization needed for a finite continuum
   quantity.

The exact admissible observables, topology, representatives, and normalization
remain part of the future proof burden.

## Vacuum Isolation Target

The key structural target is:

```text
There exists epsilon > 0 such that every non-vacuum gauge-invariant
curvature-closure class C satisfies E_closure(C) >= epsilon.
```

This is stronger than observing that a finite lattice run has a positive
effective mass. It would say the vacuum closure class is isolated from
nontrivial closed curvature excitations after renormalization and after taking
the required limits.

## Coercivity-To-Hamiltonian Step

After the Euclidean theory is constructed and Osterwalder-Schrader
reconstruction is available, one would need to establish that closure energy
controls Hamiltonian energy:

```text
E_closure(psi) >= epsilon
  -> <psi, H psi> >= Delta ||psi||^2.
```

This comparison theorem turns closure isolation into a spectral gap. Closure
energy becomes a mass-gap theorem ingredient once this comparison is established.

## Relation To Exponential Clustering

Exponential clustering is a theorem-level route with two honest forms:

1. Establish closure coercivity and Hamiltonian lower bound first, then derive
   exponential decay of connected gauge-invariant curvature correlators.
2. Establish uniform exponential decay of the Euclidean connected correlators
   directly, then use reconstruction and spectral representation to infer the
   gap.

The conjecture thesis should state which direction is being attempted.

## Finite-Lattice Diagnostic Role

The current repository tests finite-lattice shadows of this target:

- Wilson closure cost through plaquette defects,
- gauge-invariant spatial Wilson-loop operator bases,
- connected correlators,
- effective-mass diagnostics,
- quality gates,
- and packet-level candidate assessments.

These diagnostics suggest whether the closure-coercivity target is plausible
and help refine the theorem-level obligations.

## Critic's Checklist

A future proof attempt must answer:

- Is closure energy defined independently of the spectral gap?
- Is the vacuum closure class defined in gauge-invariant terms?
- Are nontrivial physical closure classes separated from vacuum by a positive
  renormalized threshold?
- Is the threshold stable under continuum and infinite-volume limits?
- Does closure energy control the reconstructed Hamiltonian energy?
- Is exponential clustering derived, or is it the independent route to the
  spectral statement?
