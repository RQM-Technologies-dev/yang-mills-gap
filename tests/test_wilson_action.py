import numpy as np

from rqm_yang_mills.gauge_field import GaugeField
from rqm_yang_mills.lattice import Lattice4D
from rqm_yang_mills.plaquette import all_closure_defects
from rqm_yang_mills.wilson_action import wilson_action


def test_wilson_action_zero_on_cold_field() -> None:
    field = GaugeField.cold(Lattice4D((2, 2, 2, 2)))
    assert wilson_action(field, beta=1.7) == 0.0


def test_wilson_action_matches_sum_of_closure_defects() -> None:
    rng = np.random.default_rng(321)
    field = GaugeField.random(Lattice4D((2, 2, 2, 2)), rng)
    beta = 2.3
    expected = beta * np.sum(all_closure_defects(field))
    assert np.isclose(wilson_action(field, beta), expected)
