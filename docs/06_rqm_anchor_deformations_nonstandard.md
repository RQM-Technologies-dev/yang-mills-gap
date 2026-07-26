# RQM Anchor Deformations Are Nonstandard

Anchor deformations are not part of standard SU(2) Wilson lattice Yang-Mills unless a separate derivation is supplied.

A toy anchor term might look like:

```text
lambda * sum_p (D_p - D_anchor)^2
```

Adding this term changes the simulated theory. It must be labeled nonstandard and kept separate from the baseline Yang-Mills implementation.

In this repository, anchor deformation appears only in:

```text
experiments/exp_006_rqm_anchor_deformation_nonstandard.py
```

Outputs from that script are exploratory comparisons, not evidence for a standard Yang-Mills mass-gap theorem.
