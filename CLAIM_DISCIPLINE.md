# Claim Discipline

This repository is a proof program, not a completed Clay Yang-Mills proof.

## Allowed Claims

- The baseline code implements finite-lattice SU(2) Wilson-action diagnostics in
  unit-quaternion coordinates.
- Plaquette holonomy, closure defect, Wilson action, Wilson loops, correlators,
  effective masses, quality gates, and candidate assessments are proof
  scaffolding.
- Curvature closure is the organizing proof target.
- Closure energy is not yet a theorem-level object; it is a non-circular target
  to be defined and proved.
- Finite-lattice results may suggest continuum spectral targets.

## Forbidden Claims

- This repo proves the Clay Yang-Mills problem.
- A finite-lattice packet proves a mass gap.
- An effective-mass plateau proves the continuum theorem.
- RQM/QSG terminology proves the theorem.
- Anchor-deformed output is evidence for standard Yang-Mills.
- The closure-coercivity lemma has been proved.
- Closure energy has already been shown to control Hamiltonian energy.

## Required Wording

Use:

- proof target
- proof program
- finite-lattice diagnostic
- proof scaffolding
- interpretation layer
- non-circular closure-energy target
- not a completed Clay proof

Avoid:

- establishes the Clay result
- derives the continuum theorem
- settles the Millennium problem
- completes the proof

## Baseline Boundary

The proof route uses the standard SU(2) Wilson-action baseline. The baseline
does not include anchor terms, resonance constraints, or deformation terms.

Allowed baseline claims:

- Unit quaternions represent SU(2) link variables.
- Plaquette holonomy is the lattice curvature object.
- `D_p = 1 - scalar_part(U_p)` is the closure defect used in the Wilson action.
- `S = beta * sum_p D_p` is the implemented Wilson action.
- Plaquette and closed Wilson-loop scalar parts are gauge invariant.

## Nonstandard Boundary

Nonstandard anchor deformations are not part of the proof route. They must
remain quarantined from baseline diagnostics and cannot be used as evidence for
the standard Yang-Mills theorem.
