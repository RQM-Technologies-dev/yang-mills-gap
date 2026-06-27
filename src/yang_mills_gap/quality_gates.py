"""Quality gates for finite-lattice spectroscopy packets."""

from __future__ import annotations

from typing import Any

import numpy as np

from .baseline_contract import BASELINE_NAME, validate_baseline_sweep_config

QUALITY_GATE_CLAIM_BOUNDARY = "quality gates are finite-lattice diagnostics only; not mass-gap evidence"


def _gate(name: str, status: str, message: str, **values: Any) -> dict[str, Any]:
    return {
        "name": name,
        "status": status,
        "message": message,
        **values,
    }


def _finite_count(values: np.ndarray) -> int:
    return int(np.count_nonzero(np.isfinite(values)))


def _finite_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if np.isfinite(number) else None


def _summary(gates: list[dict[str, Any]]) -> dict[str, Any]:
    n_pass = sum(1 for gate in gates if gate["status"] == "pass")
    n_warn = sum(1 for gate in gates if gate["status"] == "warn")
    n_fail = sum(1 for gate in gates if gate["status"] == "fail")
    if n_fail:
        interpretation_status = "blocked_by_failed_quality_gates"
    elif n_warn:
        interpretation_status = "diagnostic_with_warnings"
    else:
        interpretation_status = "diagnostic_ready"
    return {
        "interpretation_status": interpretation_status,
        "n_pass": n_pass,
        "n_warn": n_warn,
        "n_fail": n_fail,
        "claim_boundary": QUALITY_GATE_CLAIM_BOUNDARY,
    }


def evaluate_packet_quality(
    records: list[dict[str, float]],
    artifacts: dict[str, np.ndarray],
    diagnostics: dict[str, Any],
    config: dict[str, Any],
    *,
    min_measurements: int = 8,
    min_finite_correlator_values: int = 2,
    min_finite_effective_mass_values: int = 1,
) -> dict[str, Any]:
    """Evaluate whether a packet is ready for cautious diagnostic inspection."""

    if min_measurements <= 0:
        raise ValueError("min_measurements must be positive")
    if min_finite_correlator_values <= 0:
        raise ValueError("min_finite_correlator_values must be positive")
    if min_finite_effective_mass_values <= 0:
        raise ValueError("min_finite_effective_mass_values must be positive")

    gates: list[dict[str, Any]] = []
    n_measurements = len(records)
    gates.append(
        _gate(
            "measurement_count",
            "pass" if n_measurements >= min_measurements else "warn",
            "measurement count is adequate" if n_measurements >= min_measurements else "measurement count is below the preferred diagnostic floor",
            n_measurements=n_measurements,
            min_measurements=min_measurements,
        )
    )

    acceptance = np.array([record.get("acceptance_rate", np.nan) for record in records], dtype=float)
    acceptance_valid = acceptance.size > 0 and bool(np.all(np.isfinite(acceptance))) and bool(np.all((0.0 <= acceptance) & (acceptance <= 1.0)))
    gates.append(
        _gate(
            "acceptance_rates_valid",
            "pass" if acceptance_valid else "fail",
            "acceptance rates are finite probabilities" if acceptance_valid else "acceptance rates must be finite values in [0, 1]",
            mean_acceptance_rate=float(np.mean(acceptance)) if acceptance.size and np.all(np.isfinite(acceptance)) else "",
        )
    )

    action_iat = _finite_float(diagnostics.get("action", {}).get("integrated_autocorrelation_time"))
    closure_iat = _finite_float(diagnostics.get("average_closure_defect", {}).get("integrated_autocorrelation_time"))
    autocorrelation_reported = action_iat is not None and closure_iat is not None
    gates.append(
        _gate(
            "autocorrelation_reported",
            "pass" if autocorrelation_reported else "warn",
            "action and closure-defect IAT diagnostics are finite" if autocorrelation_reported else "autocorrelation diagnostics are missing or non-finite",
            action_iat="" if action_iat is None else action_iat,
            closure_iat="" if closure_iat is None else closure_iat,
        )
    )

    correlator_count = _finite_count(np.asarray(artifacts["correlator"], dtype=float))
    gates.append(
        _gate(
            "finite_correlator_values",
            "pass" if correlator_count >= min_finite_correlator_values else "fail",
            "correlator has enough finite values" if correlator_count >= min_finite_correlator_values else "correlator has too few finite values",
            finite_count=correlator_count,
            min_finite_count=min_finite_correlator_values,
        )
    )

    stderr = np.asarray(artifacts["correlator_stderr"], dtype=float)
    stderr_valid = bool(np.any(np.isfinite(stderr) & (stderr >= 0.0)))
    gates.append(
        _gate(
            "bootstrap_uncertainty_reported",
            "pass" if stderr_valid else "warn",
            "bootstrap uncertainty has finite nonnegative entries" if stderr_valid else "bootstrap uncertainty is missing or non-finite",
        )
    )

    mass_log_count = _finite_count(np.asarray(artifacts["effective_mass_log"], dtype=float))
    mass_cosh_count = _finite_count(np.asarray(artifacts["effective_mass_cosh"], dtype=float))
    mass_count = mass_log_count + mass_cosh_count
    gates.append(
        _gate(
            "finite_effective_mass_values",
            "pass" if mass_count >= min_finite_effective_mass_values else "warn",
            "at least one effective-mass estimator has finite values" if mass_count >= min_finite_effective_mass_values else "no finite effective-mass values were available",
            finite_log_count=mass_log_count,
            finite_cosh_count=mass_cosh_count,
            min_finite_count=min_finite_effective_mass_values,
        )
    )

    if "baseline" in config:
        try:
            validate_baseline_sweep_config(config)
        except ValueError as exc:
            gates.append(
                _gate(
                    "baseline_contract",
                    "fail",
                    str(exc),
                    baseline=config.get("baseline", ""),
                )
            )
        else:
            gates.append(
                _gate(
                    "baseline_contract",
                    "pass",
                    "packet config matches the standard Wilson-action baseline contract",
                    baseline=BASELINE_NAME,
                )
            )
    else:
        gates.append(
            _gate(
                "baseline_contract",
                "warn",
                "packet config does not carry explicit baseline metadata",
            )
        )

    return {
        "summary": _summary(gates),
        "gates": gates,
    }
