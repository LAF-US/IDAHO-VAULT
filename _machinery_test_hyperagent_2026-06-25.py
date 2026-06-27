"""Disposable machinery-test module (Hyperagent guest run, 2026-06-25).

Exists only to give the repo's code-review bots and CI something to chew on
before the Spelunking Census. Pure, side-effect-free, safe to delete.
Not canon; asserts no vault doctrine.
"""

from __future__ import annotations


def convergence_ratio(agreements: int, total: int) -> float:
    """Fraction of cold readers that independently surfaced a cosmology element.

    A tiny stand-in for the Spelunking Census's convergence metric.
    """
    if total <= 0:
        raise ValueError("total must be positive")
    return agreements / total


def is_load_bearing_door(convergence: float, threshold: float = 0.5) -> bool:
    """Whether an entry door reliably led readers to the shared core."""
    return convergence >= threshold


if __name__ == "__main__":
    sample = convergence_ratio(9, 13)
    print(f"convergence={sample:.2f} load_bearing={is_load_bearing_door(sample)}")
