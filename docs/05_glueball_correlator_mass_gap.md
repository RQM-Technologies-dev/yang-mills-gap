# Glueball Correlator And Mass-Gap Diagnostics

A simple glueball-like operator can be built from spatial plaquettes:

```text
O(t) = average spatial plaquette scalar on time slice t
```

The connected correlator is:

```text
C(dt) = <(O(t) - <O>)(O(t + dt) - <O>)>
```

The effective-mass diagnostic is:

```text
m_eff(t) = log(C(t) / C(t + 1))
```

On a finite lattice with short chains, this is only a diagnostic. A stable positive effective mass in a numerical experiment would not establish the Clay mass gap. It would motivate further baseline checks, finite-size studies, continuum-limit work, and analytical arguments.
