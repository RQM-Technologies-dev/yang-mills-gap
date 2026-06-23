# SU(2) As Unit Quaternions

A quaternion is represented here as:

```text
q = w + x i + y j + z k
```

with scalar-first array coordinates:

```text
[w, x, y, z]
```

Unit quaternions satisfy:

```text
w^2 + x^2 + y^2 + z^2 = 1
```

They form a group under Hamilton multiplication and provide a concrete representation of SU(2). The inverse of a unit quaternion is its conjugate:

```text
q^-1 = conj(q) = [w, -x, -y, -z]
```

In this codebase, the scalar part `w` corresponds to the normalized real trace:

```text
scalar_part(U) = 0.5 * Re Tr(U)
```

This makes the Wilson plaquette defect:

```text
D_p = 1 - scalar_part(U_p)
```

a direct unit-quaternion expression for the usual SU(2) Wilson action density.

The quaternion representation is a coordinate choice. It does not change the baseline Yang-Mills theory.
