import numpy as np
import pytest

from yang_mills_gap.gauge_field import GaugeField
from yang_mills_gap.lattice import Lattice4D
from yang_mills_gap.observables import (
    GLUEBALL_OPERATOR_SPATIAL_PLAQUETTE,
    GLUEBALL_OPERATOR_SPATIAL_WILSON_LOOPS,
    glueball_timeseries,
    spatial_wilson_loop_basis_timeseries,
)


def test_glueball_timeseries_operator_modes_are_identity_on_cold_field() -> None:
    field = GaugeField.cold(Lattice4D((2, 2, 2, 4)))

    plaquette_series = glueball_timeseries(field, operator=GLUEBALL_OPERATOR_SPATIAL_PLAQUETTE)
    loop_series = glueball_timeseries(field, operator=GLUEBALL_OPERATOR_SPATIAL_WILSON_LOOPS)

    assert plaquette_series.shape == (4,)
    assert loop_series.shape == (4,)
    assert np.allclose(plaquette_series, 1.0)
    assert np.allclose(loop_series, 1.0)


def test_glueball_timeseries_rejects_unknown_operator() -> None:
    field = GaugeField.cold(Lattice4D((1, 1, 1, 2)))

    with pytest.raises(ValueError, match="unknown glueball operator"):
        glueball_timeseries(field, operator="anchor_deformed")


def test_spatial_wilson_loop_basis_timeseries_keeps_loop_channels_separate() -> None:
    field = GaugeField.cold(Lattice4D((2, 2, 2, 4)))
    basis = spatial_wilson_loop_basis_timeseries(field)

    assert set(basis) == {"spatial_loop_1x1", "spatial_loop_1x2", "spatial_loop_2x1"}
    for series in basis.values():
        assert series.shape == (4,)
        assert np.allclose(series, 1.0)
