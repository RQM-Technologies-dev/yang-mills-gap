# Anchor Deformation Warning

RQM-inspired anchor deformations are nonstandard unless a separate derivation connects them to standard Yang-Mills theory.

The baseline Wilson action is:

```text
S = beta * sum_p (1 - scalar_part(U_p))
```

An anchor-deformed toy action might add a term such as:

```text
lambda * sum_p (D_p - D_anchor)^2
```

This changes the theory being simulated. It is not standard Wilson lattice Yang-Mills.

Any script using such a term must:

- mark the action as nonstandard,
- keep outputs separate from baseline Wilson-action outputs,
- avoid using the results as evidence of a Clay-problem proof,
- state that the experiment is exploratory and hypothesis-generating.

In this repo, `experiments/exp_006_rqm_anchor_deformation.py` follows that convention.
