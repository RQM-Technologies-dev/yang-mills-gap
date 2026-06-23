import numpy as np

from yang_mills_gap.gauge_field import GaugeField
from yang_mills_gap.lattice import Lattice4D
from yang_mills_gap.plaquette import all_closure_defects, plaquette
from yang_mills_gap.quaternions import IDENTITY


def test_identity_gauge_field_has_zero_plaquette_closure_defect() -> None:
    field = GaugeField.cold(Lattice4D((2, 2, 2, 2)))
    assert np.allclose(plaquette(field, (0, 0, 0, 0), 0, 1), IDENTITY)
    assert np.allclose(all_closure_defects(field), 0.0)
