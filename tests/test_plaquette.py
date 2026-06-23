import numpy as np

from yang_mills_gap.gauge_field import GaugeField
from yang_mills_gap.lattice import Lattice4D
from yang_mills_gap.plaquette import all_closure_defects, plaquette
from yang_mills_gap.quaternions import IDENTITY, conjugate, inverse, multiply, random_unit_quaternion, scalar_part


def test_identity_gauge_field_has_zero_plaquette_closure_defect() -> None:
    field = GaugeField.cold(Lattice4D((2, 2, 2, 2)))
    assert np.allclose(plaquette(field, (0, 0, 0, 0), 0, 1), IDENTITY)
    assert np.allclose(all_closure_defects(field), 0.0)


def test_hand_built_nontrivial_plaquette_matches_direct_product() -> None:
    rng = np.random.default_rng(2024)
    lattice = Lattice4D((2, 2, 2, 2))
    field = GaugeField.cold(lattice)
    site = (0, 0, 0, 0)
    mu = 0
    nu = 1

    u_mu_x = random_unit_quaternion(rng)
    u_nu_x_plus_mu = random_unit_quaternion(rng)
    u_mu_x_plus_nu = random_unit_quaternion(rng)
    u_nu_x = random_unit_quaternion(rng)

    field.set_link(site, mu, u_mu_x)
    field.set_link(lattice.shift(site, mu), nu, u_nu_x_plus_mu)
    field.set_link(lattice.shift(site, nu), mu, u_mu_x_plus_nu)
    field.set_link(site, nu, u_nu_x)

    expected = multiply(
        multiply(multiply(u_mu_x, u_nu_x_plus_mu), inverse(u_mu_x_plus_nu)),
        inverse(u_nu_x),
    )

    assert np.allclose(plaquette(field, site, mu, nu), expected)


def test_reversed_orientation_preserves_plaquette_scalar_part() -> None:
    rng = np.random.default_rng(2025)
    lattice = Lattice4D((2, 2, 2, 2))
    field = GaugeField.cold(lattice)
    site = (0, 0, 0, 0)
    mu = 0
    nu = 1

    for link_site, direction in [
        (site, mu),
        (lattice.shift(site, mu), nu),
        (lattice.shift(site, nu), mu),
        (site, nu),
    ]:
        field.set_link(link_site, direction, random_unit_quaternion(rng))

    forward = plaquette(field, site, mu, nu)
    reversed_orientation = conjugate(forward)

    assert np.allclose(reversed_orientation, inverse(forward))
    assert np.isclose(scalar_part(forward), scalar_part(reversed_orientation))
