import numpy as np
import pytest

from yang_mills_gap.quaternions import (
    IDENTITY,
    inverse,
    multiply,
    near_identity_random_unit_quaternion,
    norm,
    normalize,
    random_unit_quaternion,
    scalar_part,
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


def test_unit_quaternion_multiplication_preserves_norm() -> None:
    rng = np.random.default_rng(101)
    q = random_unit_quaternion(rng, shape=(16,))
    p = random_unit_quaternion(rng, shape=(16,))
    assert np.allclose(norm(multiply(q, p)), 1.0)


def test_hamilton_product_is_associative_within_tolerance() -> None:
    rng = np.random.default_rng(202)
    q = random_unit_quaternion(rng)
    p = random_unit_quaternion(rng)
    r = random_unit_quaternion(rng)
    left = multiply(multiply(q, p), r)
    right = multiply(q, multiply(p, r))
    assert np.allclose(left, right)


def test_scalar_part_is_invariant_under_conjugation() -> None:
    rng = np.random.default_rng(303)
    q = random_unit_quaternion(rng)
    p = random_unit_quaternion(rng)
    conjugated = multiply(multiply(q, p), inverse(q))
    assert np.isclose(scalar_part(conjugated), scalar_part(p))


def test_zero_norm_inputs_raise_value_error() -> None:
    zero = np.zeros(4)
    with pytest.raises(ValueError):
        normalize(zero)
    with pytest.raises(ValueError):
        inverse(zero)


def test_random_unit_quaternion_shape_handling() -> None:
    rng = np.random.default_rng(404)
    scalar = random_unit_quaternion(rng)
    batch = random_unit_quaternion(rng, shape=(2, 3))
    integer_batch = random_unit_quaternion(rng, shape=5)

    assert scalar.shape == (4,)
    assert batch.shape == (2, 3, 4)
    assert integer_batch.shape == (5, 4)
    assert np.isclose(norm(scalar), 1.0)
    assert np.allclose(norm(batch), 1.0)
    assert np.allclose(norm(integer_batch), 1.0)
