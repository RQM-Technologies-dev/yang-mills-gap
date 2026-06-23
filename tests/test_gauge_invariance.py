import numpy as np

from yang_mills_gap.gauge_field import GaugeField
from yang_mills_gap.lattice import Lattice4D
from yang_mills_gap.plaquette import plaquette
from yang_mills_gap.quaternions import random_unit_quaternion, scalar_part


def test_plaquette_scalar_part_is_local_gauge_invariant() -> None:
    rng = np.random.default_rng(789)
    lattice = Lattice4D((2, 2, 2, 2))
    field = GaugeField.random(lattice, rng)
    gauges = random_unit_quaternion(rng, lattice.shape)
    transformed = field.transformed(gauges)

    site = (1, 0, 1, 0)
    original_scalar = scalar_part(plaquette(field, site, 0, 3))
    transformed_scalar = scalar_part(plaquette(transformed, site, 0, 3))

    assert np.isclose(original_scalar, transformed_scalar)
