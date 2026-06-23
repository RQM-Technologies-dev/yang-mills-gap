"""Small-lattice Metropolis updates for baseline Wilson-action experiments."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .gauge_field import GaugeField
from .lattice import Lattice4D
from .observables import average_closure_defect, average_plaquette
from .quaternions import multiply, near_identity_random_unit_quaternion, normalize
from .wilson_action import wilson_action


@dataclass(frozen=True)
class MetropolisStats:
    accepted: int
    proposed: int

    @property
    def acceptance_rate(self) -> float:
        return 0.0 if self.proposed == 0 else self.accepted / self.proposed


def propose_link(
    current_link: np.ndarray,
    step_size: float,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """Left-multiply a link by a small random SU(2) element."""

    proposal = multiply(near_identity_random_unit_quaternion(step_size, rng), current_link)
    return normalize(proposal)


def metropolis_sweep(
    field: GaugeField,
    beta: float,
    *,
    step_size: float = 0.35,
    rng: np.random.Generator | None = None,
) -> MetropolisStats:
    """Perform one full-link Metropolis sweep.

    This implementation recomputes the full action for clarity. It is suitable
    for the small lattices used in the included sanity experiments, not for
    production-scale Markov chains.
    """

    generator = np.random.default_rng() if rng is None else rng
    accepted = 0
    proposed = 0
    current_action = wilson_action(field, beta)

    for site in field.lattice.sites():
        for mu in range(4):
            old_link = field.link(site, mu).copy()
            new_link = propose_link(old_link, step_size, generator)
            field.set_link(site, mu, new_link)
            new_action = wilson_action(field, beta)
            delta = new_action - current_action
            proposed += 1
            if delta <= 0.0 or generator.random() < np.exp(-delta):
                accepted += 1
                current_action = new_action
            else:
                field.set_link(site, mu, old_link)

    return MetropolisStats(accepted=accepted, proposed=proposed)


def run_metropolis(
    lattice: Lattice4D,
    beta: float,
    *,
    n_sweeps: int,
    step_size: float = 0.35,
    thermalization: int = 0,
    measure_every: int = 1,
    hot_start: bool = False,
    seed: int | None = None,
) -> tuple[GaugeField, list[dict[str, float]]]:
    """Run a small Metropolis chain and return the final field plus records."""

    if n_sweeps < 0:
        raise ValueError("n_sweeps must be nonnegative")
    if thermalization < 0:
        raise ValueError("thermalization must be nonnegative")
    if measure_every <= 0:
        raise ValueError("measure_every must be positive")

    rng = np.random.default_rng(seed)
    field = GaugeField.random(lattice, rng) if hot_start else GaugeField.cold(lattice)
    records: list[dict[str, float]] = []

    for sweep in range(1, n_sweeps + 1):
        stats = metropolis_sweep(field, beta, step_size=step_size, rng=rng)
        if sweep > thermalization and (sweep - thermalization) % measure_every == 0:
            records.append(
                {
                    "sweep": float(sweep),
                    "action": wilson_action(field, beta),
                    "average_plaquette": average_plaquette(field),
                    "average_closure_defect": average_closure_defect(field),
                    "acceptance_rate": stats.acceptance_rate,
                }
            )

    return field, records
