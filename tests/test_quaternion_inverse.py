import numpy as np

from rqm_yang_mills.quaternions import IDENTITY, inverse, multiply, random_unit_quaternion


def test_quaternion_inverse_multiplies_to_identity() -> None:
    rng = np.random.default_rng(456)
    q = random_unit_quaternion(rng)
    assert np.allclose(multiply(q, inverse(q)), IDENTITY)
    assert np.allclose(multiply(inverse(q), q), IDENTITY)
