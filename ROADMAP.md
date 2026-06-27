# Roadmap

## Phase 1: Standard SU(2) Lattice Baseline

- Implement NumPy unit-quaternion utilities.
- Build a periodic 4D lattice helper.
- Store SU(2) gauge fields as unit-quaternion link variables.
- Compute plaquette holonomy, closure defect, and Wilson action.
- Add gauge-invariant observables, full-action reference Metropolis updates, and local staple-based Metropolis updates.
- Keep packetized spectroscopy runs tied to an explicit standard Wilson-action baseline contract.
- Verify quaternion identities, plaquette identity behavior, gauge invariance, Wilson-loop invariance, nonnegative Wilson action, and local action differences.

## Phase 2: Baseline Numerical Quality

- Treat current experiments as tiny finite-lattice sanity diagnostics.
- Add autocorrelation estimates and thermalization diagnostics before interpreting long chains.
- Use bootstrap or jackknife errors for correlators and effective-mass diagnostics.
- Compare full-action and local-action Metropolis paths on tiny lattices as an implementation sanity check.
- Wrap finite-lattice sanity runs in diagnostic packets with config, observables, diagnostics, and plots.
- Report packet-level quality gates before interpreting correlators or effective masses.
- Maintain separate packet examples for observable diagnostics and correlator/effective-mass diagnostics.
- Add packet comparison and beta/seed sweep diagnostics.
- Add plateau heuristic diagnostics for candidate flat effective-mass windows while keeping them explicitly non-proof diagnostics.
- Explore beta and lattice-size dependence.
- Add modest larger spectroscopy sweeps with configurable run parameters and improved baseline measurement operators.
- Move from smoke-test lattices to larger volumes only after baseline diagnostics are stable.

## Phase 3: Glueball-Like Correlators

- Run larger lattice sweeps once the packet pipeline is stable.
- Refine spatial plaquette operators and develop improved glueball operators.
- Compare 1x1 spatial plaquette operators against small spatial Wilson-loop operator bases.
- Improve connected correlator statistics.
- Fit effective-mass plateaus with uncertainty estimates.
- Compare finite-volume and finite-spacing behavior with larger lattice and finite-volume checks.
- Require larger lattices, thermalization checks, autocorrelation estimates, and uncertainty analysis before treating an effective-mass plateau as physically meaningful.
- Treat effective-mass plots as diagnostics only until thermalization, autocorrelation, and uncertainty checks are reported beside them.
- Require an accompanying diagnostic packet before comparing effective-mass plots across runs.
- Keep correlator/effective-mass packets clearly labeled as finite-lattice diagnostics, not Clay mass-gap results.

## Phase 4: RQM Interpretation Layer

- Map plaquette holonomy to curvature closure.
- Map Wilson action to closure cost.
- Interpret the mass-gap target as the lowest nonzero closed gauge-invariant curvature resonance.
- Develop the RQM closure-resonance interpretation as a working hypothesis over standard gauge-invariant packet outputs.
- Maintain `docs/08_closure_resonance_roadmap.md` as the dedicated closure-resonance interpretation document connecting packet diagnostics to precise future analytical targets.
- Keep the interpretation separate from deformed dynamics.

## Phase 5: Nonstandard Anchor Deformations

- Explore anchor terms only in explicitly labeled nonstandard experiments.
- Compare deformed dynamics against the baseline without merging claims.
- Treat these experiments as hypothesis generators, not theorem evidence.
- Do not merge anchor terms into the baseline Wilson action.

## Phase 6: Proof Roadmap

- Document what would be required for a continuum construction.
- Maintain `docs/07_proof_roadmap.md` as the proof-gap register separating finite-lattice diagnostics from missing analytical obligations.
- Track the gaps between finite-lattice numerics and rigorous spectral claims.
- Keep proof-oriented language conditional until each analytical step is supplied.
- Convert finite-lattice closure-resonance candidates into precise continuum/proof targets only after baseline numerical behavior is auditable.
