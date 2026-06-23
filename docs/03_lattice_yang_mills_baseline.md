# Lattice Yang-Mills Baseline

The baseline model is standard SU(2) Wilson lattice Yang-Mills on a periodic four-dimensional lattice.

The lattice coordinate order is:

```text
(x, y, z, t)
```

Each link variable is a unit quaternion:

```text
U[x, y, z, t, mu]
```

where `mu` is one of the four lattice directions.

For directions `mu != nu`, the plaquette is:

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

No RQM anchor term, closure penalty, or deformation is present in the baseline action.

Local gauge transformations act as:

```text
U_mu(x) -> g(x) U_mu(x) g^-1(x + mu)
```

Under this transformation, the plaquette holonomy transforms by conjugation at its base point. Its scalar part is invariant. The tests verify this finite-lattice property.
