"""Reusable Matplotlib plots for diagnostic packets."""

from __future__ import annotations

import numpy as np


def plot_running_mean(values, running_values, ylabel: str, title: str):
    import matplotlib.pyplot as plt

    x = np.arange(len(values))
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(x, values, marker="o", linewidth=1.0, label=ylabel)
    ax.plot(x, running_values, linewidth=1.8, label="running mean")
    ax.set_xlabel("measurement")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    return fig


def plot_autocorrelation(values, ylabel: str, title: str):
    import matplotlib.pyplot as plt

    x = np.arange(len(values))
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.axhline(0.0, color="black", linewidth=0.8)
    ax.plot(x, values, marker="o", linewidth=1.2)
    ax.set_xlabel("lag")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    fig.tight_layout()
    return fig


def plot_thermalization(windows, ylabel: str, title: str):
    import matplotlib.pyplot as plt

    cuts = [row["cut_fraction"] for row in windows]
    means = [row["mean"] for row in windows]
    stderr = [row["stderr"] for row in windows]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.errorbar(cuts, means, yerr=stderr, marker="o", capsize=3)
    ax.set_xlabel("discarded fraction")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    fig.tight_layout()
    return fig


def plot_correlator(correlator, stderr):
    import matplotlib.pyplot as plt

    x = np.arange(len(correlator))
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.errorbar(x, correlator, yerr=stderr, marker="o", capsize=3)
    ax.axhline(0.0, color="black", linewidth=0.8)
    ax.set_xlabel("temporal separation")
    ax.set_ylabel("connected C(t)")
    ax.set_title("Glueball-like correlator diagnostic")
    fig.tight_layout()
    return fig


def plot_effective_mass(mass_log, mass_cosh):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(np.arange(len(mass_log)), mass_log, marker="o", label="log")
    ax.plot(np.arange(len(mass_cosh)), mass_cosh, marker="s", label="cosh")
    ax.set_xlabel("t")
    ax.set_ylabel("m_eff(t)")
    ax.set_title("Effective-mass diagnostic")
    ax.legend()
    fig.tight_layout()
    return fig
