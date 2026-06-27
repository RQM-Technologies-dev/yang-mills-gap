import numpy as np

from yang_mills_gap.gauge_field import GaugeField
from yang_mills_gap.lattice import Lattice4D
from yang_mills_gap.observables import spatial_wilson_loop_basis_timeseries, wilson_loop_scalar
from yang_mills_gap.plaquette import all_plaquette_scalars, plaquette
from yang_mills_gap.quaternions import random_unit_quaternion, scalar_part
from yang_mills_gap.wilson_action import wilson_action


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


def test_all_plaquette_scalar_parts_are_local_gauge_invariant() -> None:
    rng = np.random.default_rng(790)
    lattice = Lattice4D((2, 2, 2, 2))
    field = GaugeField.random(lattice, rng)
    transformed = field.transformed(random_unit_quaternion(rng, lattice.shape))

    assert np.allclose(all_plaquette_scalars(field), all_plaquette_scalars(transformed))


def test_wilson_action_is_local_gauge_invariant() -> None:
    rng = np.random.default_rng(791)
    lattice = Lattice4D((2, 2, 2, 2))
    field = GaugeField.random(lattice, rng)
    transformed = field.transformed(random_unit_quaternion(rng, lattice.shape))

    assert np.isclose(wilson_action(field, beta=2.1), wilson_action(transformed, beta=2.1))


def test_rectangular_wilson_loop_scalar_is_local_gauge_invariant() -> None:
    rng = np.random.default_rng(792)
    lattice = Lattice4D((3, 3, 3, 3))
    field = GaugeField.random(lattice, rng)
    transformed = field.transformed(random_unit_quaternion(rng, lattice.shape))

    original_loop = wilson_loop_scalar(field, (1, 0, 2, 1), 0, 3, 2, 1)
    transformed_loop = wilson_loop_scalar(transformed, (1, 0, 2, 1), 0, 3, 2, 1)

    assert np.isclose(original_loop, transformed_loop)


def test_spatial_wilson_loop_basis_is_local_gauge_invariant() -> None:
    rng = np.random.default_rng(793)
    lattice = Lattice4D((3, 3, 3, 3))
    field = GaugeField.random(lattice, rng)
    transformed = field.transformed(random_unit_quaternion(rng, lattice.shape))

    original_basis = spatial_wilson_loop_basis_timeseries(field)
    transformed_basis = spatial_wilson_loop_basis_timeseries(transformed)

    assert original_basis.keys() == transformed_basis.keys()
    for key in original_basis:
        assert np.allclose(original_basis[key], transformed_basis[key])
