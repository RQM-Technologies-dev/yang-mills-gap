import numpy as np

from rqm_yang_mills.gauge_field import GaugeField
from rqm_yang_mills.lattice import Lattice4D
from rqm_yang_mills.plaquette import all_closure_defects, plaquette
from rqm_yang_mills.quaternions import IDENTITY


def test_cold_field_plaquette_is_identity() -> None:
    field = GaugeField.cold(Lattice4D((2, 2, 2, 2)))
    assert np.allclose(plaquette(field, (0, 0, 0, 0), 0, 1), IDENTITY)
    assert np.allclose(all_closure_defects(field), 0.0)
