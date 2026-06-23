import numpy as np

from yang_mills_gap.gauge_field import GaugeField
from yang_mills_gap.lattice import Lattice4D
from yang_mills_gap.wilson_action import wilson_action


def test_wilson_action_is_nonnegative() -> None:
    rng = np.random.default_rng(321)
    field = GaugeField.random(Lattice4D((2, 2, 2, 2)), rng)
    assert wilson_action(field, beta=2.3) >= 0.0


def test_wilson_action_zero_on_identity_field() -> None:
    field = GaugeField.cold(Lattice4D((2, 2, 2, 2)))
    assert wilson_action(field, beta=1.7) == 0.0
