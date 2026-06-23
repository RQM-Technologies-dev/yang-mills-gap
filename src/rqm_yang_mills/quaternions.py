"""Unit-quaternion utilities for SU(2) link variables.

Quaternions are represented as NumPy arrays with scalar-first coordinates
``[w, x, y, z]``. Unit quaternions double-cover SU(2), and the scalar part is
the normalized fundamental trace: ``0.5 * Re Tr(U)``.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray

QuaternionArray = NDArray[np.float64]

IDENTITY: QuaternionArray = np.array([1.0, 0.0, 0.0, 0.0], dtype=float)


def as_quaternion(q: ArrayLike) -> QuaternionArray:
    """Return ``q`` as a floating NumPy array with final dimension 4."""

    arr = np.asarray(q, dtype=float)
    if arr.shape[-1:] != (4,):
        raise ValueError(f"expected final quaternion dimension 4, got {arr.shape}")
    return arr


def norm(q: ArrayLike) -> QuaternionArray:
    """Return the Euclidean quaternion norm along the final axis."""

    arr = as_quaternion(q)
    return np.linalg.norm(arr, axis=-1)


def normalize(q: ArrayLike, *, eps: float = 1e-14) -> QuaternionArray:
    """Normalize one or more quaternions.

    Raises:
        ValueError: if any quaternion has near-zero norm.
    """

    arr = as_quaternion(q)
    norms = np.linalg.norm(arr, axis=-1, keepdims=True)
    if np.any(norms < eps):
        raise ValueError("cannot normalize a zero-norm quaternion")
    return arr / norms


def multiply(a: ArrayLike, b: ArrayLike) -> QuaternionArray:
    """Hamilton product of scalar-first quaternions."""

    qa = as_quaternion(a)
    qb = as_quaternion(b)
    aw, ax, ay, az = np.moveaxis(qa, -1, 0)
    bw, bx, by, bz = np.moveaxis(qb, -1, 0)
    return np.stack(
        [
            aw * bw - ax * bx - ay * by - az * bz,
            aw * bx + ax * bw + ay * bz - az * by,
            aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw,
        ],
        axis=-1,
    )


def conjugate(q: ArrayLike) -> QuaternionArray:
    """Quaternion conjugate."""

    arr = as_quaternion(q)
    result = np.array(arr, copy=True)
    result[..., 1:] *= -1.0
    return result


def inverse(q: ArrayLike, *, eps: float = 1e-14) -> QuaternionArray:
    """Multiplicative inverse of one or more quaternions."""

    arr = as_quaternion(q)
    norm_sq = np.sum(arr * arr, axis=-1, keepdims=True)
    if np.any(norm_sq < eps):
        raise ValueError("cannot invert a zero-norm quaternion")
    return conjugate(arr) / norm_sq


def random_unit_quaternion(
    rng: np.random.Generator | None = None,
    shape: int | tuple[int, ...] = (),
) -> QuaternionArray:
    """Sample unit quaternions from normalized Gaussian coordinates."""

    generator = np.random.default_rng() if rng is None else rng
    sample_shape = (shape,) if isinstance(shape, int) else tuple(shape)
    raw = generator.normal(size=sample_shape + (4,))
    return normalize(raw)


def scalar_part(q: ArrayLike) -> QuaternionArray:
    """Return the scalar component ``w``."""

    return as_quaternion(q)[..., 0]


def near_identity(
    step_size: float,
    rng: np.random.Generator | None = None,
) -> QuaternionArray:
    """Sample a small SU(2) proposal close to the identity.

    ``step_size`` bounds the physical rotation angle used in the exponential
    parameterization. The result is a unit quaternion.
    """

    if step_size < 0:
        raise ValueError("step_size must be nonnegative")
    generator = np.random.default_rng() if rng is None else rng
    axis = generator.normal(size=3)
    axis_norm = np.linalg.norm(axis)
    if axis_norm < 1e-14:
        axis = np.array([1.0, 0.0, 0.0])
    else:
        axis = axis / axis_norm
    angle = generator.uniform(-step_size, step_size)
    half_angle = 0.5 * angle
    return np.array(
        [np.cos(half_angle), *(np.sin(half_angle) * axis)],
        dtype=float,
    )
