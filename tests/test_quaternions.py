import numpy as np

from yang_mills_gap.quaternions import (
    IDENTITY,
    inverse,
    multiply,
    near_identity_random_unit_quaternion,
    norm,
    normalize,
    random_unit_quaternion,
)


def test_quaternion_norm_preservation() -> None:
    rng = np.random.default_rng(123)
    q = random_unit_quaternion(rng, shape=(32,))
    assert np.allclose(norm(q), 1.0)
    assert np.isclose(norm(normalize(np.array([2.0, -3.0, 4.0, 1.0]))), 1.0)


def test_inverse_multiplies_to_identity() -> None:
    rng = np.random.default_rng(456)
    q = random_unit_quaternion(rng)
    assert np.allclose(multiply(q, inverse(q)), IDENTITY)
    assert np.allclose(multiply(inverse(q), q), IDENTITY)


def test_near_identity_random_unit_quaternion_has_unit_norm() -> None:
    rng = np.random.default_rng(789)
    q = near_identity_random_unit_quaternion(0.25, rng)
    assert np.isclose(norm(q), 1.0)
