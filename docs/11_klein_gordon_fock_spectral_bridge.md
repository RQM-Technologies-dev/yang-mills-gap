# Klein–Gordon–Fock as the Spectral Reference Bridge

## 1. Purpose

This document does not propose Klein–Gordon–Fock (KGF) as the origin of the
Yang–Mills mass gap. It uses the massive scalar field as the canonical control
model for the long-distance correlator behavior expected when a gauge-invariant
scalar excitation with positive mass dominates.

KGF is a reference model. It does not prove a positive Yang–Mills threshold.
The curvature closure conjecture is the proposed mechanism that could explain
why pure quantum Yang–Mills has a positive lowest physical energy.

## 2. What Klein–Gordon–Fock Describes

The KGF equation describes relativistic propagation of a spin-zero field. In
units with the speed of light and Planck's constant set to one, its Lorentzian
form is

```text
(Box + m^2) phi = 0.
```

The mass `m` is already supplied to this equation. It introduces a finite
inverse length scale rather than explaining where that scale came from. After
continuation to Euclidean time, a single zero-momentum state contributes

```text
C(t) = A exp(-m t).
```

On a lattice with periodic temporal extent `T`, forward and backward Euclidean
propagation combine:

```text
C_T(t) = A [exp(-m t) + exp(-m (T - t))]
       = 2 A exp(-m T/2) cosh(m (T/2 - t)).
```

These forms motivate the repository's logarithmic estimator

```text
m_eff(t) = log(C(t) / C(t+1))
```

and periodic cosh estimator

```text
m_eff(t) = arccosh((C(t-1) + C(t+1)) / (2 C(t))).
```

They are calibration identities under single-state dominance, not a derivation
of a Yang–Mills mass.

## 3. What the Yang–Mills Problem Asks Instead

Classical pure Yang–Mills theory has non-Abelian gauge connections, curvature,
and nonlinear gauge dynamics, but no conventional gauge-boson mass term. The
mass-gap problem asks why the gauge-invariant quantum spectrum has a strictly
positive threshold above its vacuum.

Inserting a KGF mass term would change the theory and would not solve the Clay
problem. The relevant physical excitations are gauge-invariant composites, not
free elementary scalar fields. A scalar glueball-like operator can transform as
a scalar without making the state a fundamental KGF field.

## 4. Gauge-Invariant Correlator Bridge

For a suitable gauge-invariant curvature operator `O`, the spectral chain is:

```text
gauge-invariant curvature operator
  -> acts on the vacuum
  -> creates a superposition of physical gauge-invariant states
  -> Euclidean two-point correlator
  -> spectral sum of decaying contributions
  -> lowest state with nonzero operator overlap dominates at large separation
  -> single exponential or periodic cosh behavior if an isolated scalar state dominates
```

Schematically, a connected correlator has contributions

```text
C(t) = sum_n |<n|O|Omega>|^2 exp(-(E_n - E_0)t),
```

with periodic backward terms at finite `T`. The repository's correlator,
effective-mass, and plateau code tests finite-lattice shadows of this chain.
Synthetic KGF correlators validate estimator behavior when the answer is known;
Yang–Mills correlators remain separate finite-lattice diagnostics.

Osterwalder–Schrader reconstruction, together with the required Euclidean
axioms including reflection positivity, is the theorem-level bridge to a
physical Hilbert space, vacuum, Hamiltonian, and spectrum. A KGF analogy does
not replace that bridge.

## 5. Relationship to Curvature Closure

Curvature closure is the proposed origin of the positive threshold.
Klein–Gordon–Fock describes the propagation signature expected after such a
positive threshold exists.

| Layer | Role |
| --- | --- |
| Wilson-action lattice baseline | Standard finite-lattice Yang–Mills dynamics |
| Curvature-closure conjecture | Proposed mechanism for positive minimum non-vacuum energy |
| KGF reference model | Canonical massive scalar correlator behavior |
| Effective-mass diagnostics | Finite-lattice estimator of the dominant decay scale |
| Osterwalder–Schrader reconstruction | Theorem-level Euclidean-to-Hamiltonian bridge |
| Spectral theorem | Final positive-gap conclusion after obligations are met |

## 6. What “Balance” Means Here

Disciplined uses of balance are limited. Relativistic propagation balances
temporal and spatial variation. Periodic Euclidean correlators include forward
and backward propagation. Positive- and negative-frequency sectors belong to
the complete relativistic field. A massive mode introduces a finite intrinsic
scale.

None of these statements says that two waves balancing causes the Yang–Mills
mass gap, that particle/antiparticle balance creates a glueball mass, that a
“one-half balance” explains the threshold, or that the KGF equation proves
closure coercivity.

## 7. Mass Gap Versus Isolated Particle

A mass gap means that the physical spectrum has no values arbitrarily close to
the vacuum. An isolated one-particle state is a stronger statement. A clean
effective-mass plateau is most naturally associated with dominance by one
state, but a continuum theory can have a gap even if its lowest spectral
contribution is not an ideal free-scalar pole.

Finite-volume spectra are discrete. Any physical conclusion additionally
requires control of lattice spacing, volume, operator overlap, uncertainty,
continuum limits, infinite-volume limits, and reconstruction.

## 8. Claim Boundary

### Forbidden claims

- “Klein–Gordon–Fock proves the Yang–Mills mass gap.”
- “Adding a scalar mass solves pure Yang–Mills.”
- “The glueball is fundamentally a free Klein–Gordon field.”
- “A cosh fit proves the continuum gap.”
- “The effective-mass plateau is the Clay mass gap.”
- “KGF establishes closure coercivity.”
- “Gauge bosons simply become Klein–Gordon particles.”
- “Curvature closure has already been derived from KGF.”

These sentences delimit claims and must not be asserted as repository results.
The executable KGF layer is diagnostic only and never changes the standard
SU(2) Wilson-action dynamics.

## 9. Correct Summary Statement

The Klein–Gordon–Fock field is used here as a spectral calibration and
long-distance reference model. It shows what positive mass looks like in
relativistic propagation and Euclidean correlation decay. The curvature-closure
conjecture separately proposes why the lowest nontrivial gauge-invariant
Yang–Mills excitation may be unable to approach zero energy. Connecting that
conjectural closure threshold to the reconstructed Yang–Mills Hamiltonian
remains a theorem-level obligation.
