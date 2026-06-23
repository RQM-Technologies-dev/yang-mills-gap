import numpy as np
import pytest

from yang_mills_gap.gauge_field import GaugeField
from yang_mills_gap.lattice import Lattice4D
from yang_mills_gap.monte_carlo import metropolis_sweep_local, propose_link
from yang_mills_gap.wilson_action import local_wilson_action_contribution, staple_sum, wilson_action


def test_wilson_action_is_nonnegative() -> None:
    rng = np.random.default_rng(321)
    field = GaugeField.random(Lattice4D((2, 2, 2, 2)), rng)
    assert wilson_action(field, beta=2.3) >= 0.0


def test_wilson_action_zero_on_identity_field() -> None:
    field = GaugeField.cold(Lattice4D((2, 2, 2, 2)))
    assert wilson_action(field, beta=1.7) == 0.0


def test_staple_sum_has_quaternion_shape() -> None:
    rng = np.random.default_rng(654)
    field = GaugeField.random(Lattice4D((2, 2, 2, 2)), rng)
    assert staple_sum(field, (0, 1, 0, 1), 2).shape == (4,)


def test_local_action_validates_beta_and_direction() -> None:
    field = GaugeField.cold(Lattice4D((2, 2, 2, 2)))
    site = (0, 0, 0, 0)

    with pytest.raises(ValueError):
        wilson_action(field, beta=-1.0)
    with pytest.raises(ValueError):
        local_wilson_action_contribution(field, site, 0, beta=-1.0)
    with pytest.raises(ValueError):
        staple_sum(field, site, 4)
    with pytest.raises(ValueError):
        local_wilson_action_contribution(field, site, 4, beta=1.0)


def test_local_action_rejects_nonunit_or_malformed_proposed_link() -> None:
    rng = np.random.default_rng(655)
    field = GaugeField.random(Lattice4D((2, 2, 2, 2)), rng)
    site = (0, 1, 0, 1)
    mu = 2
    unit_link = propose_link(field.link(site, mu), step_size=0.25, rng=rng)
    scaled_link = 3.0 * unit_link

    assert np.isfinite(local_wilson_action_contribution(field, site, mu, beta=2.0, link=unit_link))
    with pytest.raises(ValueError):
        local_wilson_action_contribution(field, site, mu, beta=2.0, link=scaled_link)
    with pytest.raises(ValueError):
        local_wilson_action_contribution(field, site, mu, beta=2.0, link=np.ones((2, 4)))


def test_local_action_difference_matches_full_action_difference() -> None:
    rng = np.random.default_rng(987)
    beta = 1.9
    lattice = Lattice4D((3, 3, 3, 3))

    for _ in range(6):
        field = GaugeField.random(lattice, rng)
        site = tuple(int(rng.integers(0, extent)) for extent in lattice.shape)
        mu = int(rng.integers(0, lattice.ndim))
        old_link = field.link(site, mu).copy()
        proposed_link = propose_link(old_link, step_size=0.35, rng=rng)

        old_full_action = wilson_action(field, beta)
        old_local_action = local_wilson_action_contribution(field, site, mu, beta)
        new_local_action = local_wilson_action_contribution(
            field,
            site,
            mu,
            beta,
            link=proposed_link,
        )

        field.set_link(site, mu, proposed_link)
        new_full_action = wilson_action(field, beta)

        assert np.isclose(new_full_action - old_full_action, new_local_action - old_local_action)


def test_local_metropolis_sweep_preserves_unit_norms() -> None:
    rng = np.random.default_rng(988)
    field = GaugeField.random(Lattice4D((2, 2, 2, 2)), rng)
    stats = metropolis_sweep_local(field, beta=2.0, step_size=0.25, rng=rng)

    assert stats.proposed == field.lattice.volume * field.lattice.ndim
    assert 0 <= stats.acceptance_rate <= 1
    assert np.allclose(np.linalg.norm(field.links, axis=-1), 1.0)
