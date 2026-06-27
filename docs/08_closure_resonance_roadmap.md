# Closure-Resonance Roadmap

## Purpose

This document connects the repository's finite-lattice packet diagnostics to the
RQM/QSG closure-resonance interpretation and to later analytical targets.

The goal is to keep one bridge document between:

- standard SU(2) Wilson lattice Yang-Mills diagnostics,
- the RQM/QSG interpretation of those diagnostics as curvature closure and
  resonance probes,
- and the future proof-facing questions that would be required before any
  continuum mass-gap claim could be made.

## Claim Boundary

This repository is not a Clay Yang-Mills mass-gap proof. It is not a
continuum construction of four-dimensional quantum Yang-Mills theory.

The current work is an exploratory finite-lattice sandbox. Packet outputs,
effective-mass plots, plateau heuristics, and beta/seed comparisons are
diagnostics for the implementation and for the working hypothesis. They do not
establish the Yang-Mills mass gap.

The baseline implementation must remain standard SU(2) Wilson lattice
Yang-Mills. RQM/QSG language is an interpretation layer over gauge-invariant
baseline outputs unless a separate nonstandard experiment is explicitly labeled
as such.

## Baseline Objects

The baseline uses scalar-first unit quaternions as coordinates for SU(2) link
variables:

```text
U[x, y, z, t, mu]
```

Plaquette holonomy is the local lattice curvature object:

```text
U_mu(x) U_nu(x + mu) U_mu^-1(x + nu) U_nu^-1(x)
```

The closure defect is:

```text
D_p = 1 - scalar_part(U_p)
```

The Wilson action is:

```text
S = beta * sum_p D_p
```

Glueball-like operators are built from closed spatial gauge-invariant loops,
including spatial plaquettes and small spatial Wilson-loop averages. Connected
temporal correlators compare those operators across time separation. Log and
cosh effective-mass estimators are finite-lattice diagnostics extracted from
those correlators.

## RQM/QSG Dictionary

The working dictionary is:

- Plaquette holonomy is interpreted as non-abelian curvature closure.
- Closure defect measures local failure of the plaquette holonomy to close to
  the identity.
- Wilson action is interpreted as the standard Yang-Mills closure cost.
- Closed spatial Wilson loops are gauge-invariant curvature probes.
- Connected correlators are finite-lattice resonance diagnostics.
- Effective mass is a finite-lattice diagnostic for candidate spectral
  behavior.
- The mass-gap target is interpreted as the lowest nonzero closed,
  gauge-invariant, non-abelian curvature resonance.

This dictionary does not deform the baseline action or update rule. It gives
RQM/QSG names to standard gauge-invariant Yang-Mills objects so the repository
can ask sharper questions without merging interpretation into evidence.

## Packet Diagnostics To Research Questions

Run packets make the baseline auditable. A useful packet records the run
configuration, measured observables, diagnostics, correlators, effective-mass
tables, plots, and any packet-local notes needed to understand failures.

The packet pipeline should answer research questions such as:

- Do the standard Wilson-action observables behave consistently across seeds?
- Are thermalization and autocorrelation warnings visible before correlator
  interpretation?
- Do bootstrap or jackknife uncertainty helpers report stable enough errors to
  compare runs?
- Do beta/seed sweeps reduce sparse or invalid effective-mass estimates?
- Do plateau heuristics identify candidate windows, and do those candidates
  survive uncertainty and seed checks?
- Do richer gauge-invariant operator choices improve signal quality without
  changing the action?

Positive answers sharpen the closure-resonance hypothesis. Negative answers
are also useful because they identify numerical or operator-basis weaknesses.
Neither kind of answer is continuum proof evidence by itself.

## Near-Term Numerical Roadmap

Near-term work should improve numerical trust before interpretive weight:

- Keep local Metropolis updates and Wilson action dynamics as the standard
  baseline.
- Report thermalization and autocorrelation diagnostics beside correlator and
  effective-mass outputs.
- Expand uncertainty reporting for correlators, effective masses, and plateau
  candidates.
- Compare stronger gauge-invariant operator bases before changing dynamics,
  including separate spatial Wilson-loop channels before averaging them.
- Run longer chains only when diagnostics and packet writing remain stable.
- Move to larger lattices gradually, with finite-volume checks rather than
  isolated larger runs.
- Compare beta, seed, volume, and operator dependence in packetized sweeps.
- Treat plateau candidates as provisional until uncertainty-backed fits and
  cross-run stability are available.

The immediate practical target is not "find the mass gap." It is to make the
finite-lattice spectroscopy pipeline honest enough that a candidate
closure-resonance signal would be auditable.

A packet-level candidate should require explicit quality-gate output, finite
effective-mass values, a positive plateau candidate, and recorded reasons when
any of those checks fail. This remains a finite-lattice diagnostic label, not a
continuum spectral claim.

## Analytical Targets

The proof-facing program remains future work. It would need at least:

- a controlled continuum limit,
- an infinite-volume limit,
- a gauge-invariant observable framework compatible with the continuum theory,
- a Hilbert-space or spectral formulation for the physical states,
- control of the transfer-matrix or Hamiltonian spectrum,
- a definition of the vacuum and lowest non-vacuum gauge-invariant sector,
- and a proof that the lowest non-vacuum gauge-invariant energy is strictly
  positive.

Finite-lattice closure-resonance candidates can help name and organize these
targets. They do not replace them.

## Nonstandard Deformation Boundary

Anchor deformations are nonstandard experiments. They may be useful as
hypothesis generators, but they change the simulated theory.

Anchor-deformed outputs must not be merged into baseline Wilson-action
evidence. They cannot be used as evidence for the standard Yang-Mills theorem
unless a separate derivation shows why the deformed dynamics are equivalent to
the standard target.

## Acceptance Standard

The repository can make stronger finite-lattice claims only when the supporting
packet evidence includes:

- reproducible run packets with configs, diagnostics, correlators,
  effective-mass tables, and plots,
- stable diagnostics across beta, seed, volume, and operator choices,
- thermalization and autocorrelation checks reported beside spectroscopy
  outputs,
- uncertainty estimates for correlators, effective masses, and plateau fits,
- documented failures and weak signals, not only successful plots,
- and unchanged baseline Wilson-action dynamics.

Even then, the result would remain a finite-lattice diagnostic claim until the
analytical targets above are supplied.
