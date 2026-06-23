# Lattice Yang-Mills Baseline

The baseline is standard SU(2) Wilson lattice Yang-Mills on a periodic four-dimensional lattice with coordinate order:

```text
(x, y, z, t)
```

Each link variable is a unit quaternion:

```text
U[x, y, z, t, mu]
```

where `mu` is in `0..3`.

Local gauge transformations act as:

```text
U_mu(x) -> g(x) U_mu(x) g^-1(x + mu)
```

The baseline implementation preserves unit norm and tests gauge invariance of plaquette scalar parts. RQM deformation terms are not part of this baseline.
