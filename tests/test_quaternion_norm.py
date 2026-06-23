import numpy as np

from rqm_yang_mills.quaternions import norm, normalize, random_unit_quaternion


def test_normalize_returns_unit_quaternion() -> None:
    q = normalize(np.array([2.0, -3.0, 4.0, 1.0]))
    assert np.isclose(norm(q), 1.0)


def test_random_unit_quaternion_batch_has_unit_norm() -> None:
    rng = np.random.default_rng(123)
    q = random_unit_quaternion(rng, shape=(32,))
    assert np.allclose(norm(q), 1.0)
