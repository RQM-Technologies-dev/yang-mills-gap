import numpy as np

from rqm_yang_mills.gauge_field import GaugeField
from rqm_yang_mills.lattice import Lattice4D
from rqm_yang_mills.observables import average_plaquette
from rqm_yang_mills.plaquette import plaquette
from rqm_yang_mills.quaternions import random_unit_quaternion, scalar_part
from rqm_yang_mills.wilson_action import wilson_action


def test_plaquette_scalar_is_gauge_invariant() -> None:
    rng = np.random.default_rng(789)
    lattice = Lattice4D((2, 2, 2, 2))
    field = GaugeField.random(lattice, rng)
    gauges = random_unit_quaternion(rng, lattice.shape)
    transformed = field.transformed(gauges)

    site = (1, 0, 1, 0)
    original_scalar = scalar_part(plaquette(field, site, 0, 3))
    transformed_scalar = scalar_part(plaquette(transformed, site, 0, 3))

    assert np.isclose(original_scalar, transformed_scalar)
    assert np.isclose(average_plaquette(field), average_plaquette(transformed))
    assert np.isclose(wilson_action(field, beta=2.1), wilson_action(transformed, beta=2.1))
