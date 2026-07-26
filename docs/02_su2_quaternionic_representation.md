# SU(2) Quaternionic Representation

Quaternions are stored as scalar-first arrays:

```text
[w, x, y, z]
```

corresponding to:

```text
q = w + x i + y j + z k
```

Unit quaternions satisfy:

```text
w^2 + x^2 + y^2 + z^2 = 1
```

The unit quaternions form a group under Hamilton multiplication and represent SU(2). In this coordinate system, the scalar part is the normalized real fundamental trace:

```text
scalar_part(U) = 0.5 * Re Tr(U)
```

This is a representation choice for the standard baseline. It does not deform Yang-Mills theory.
