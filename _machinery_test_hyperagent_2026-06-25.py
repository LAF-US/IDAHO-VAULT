"""Disposable machinery-test module (Hyperagent guest run, 2026-06-25).

A small, side-effect-free helper for measuring how much independent cold
readers agree — the core metric for the Spelunking Census. Safe to delete;
not canon.

Research note (2026-06-25): "do N readers independently agree on a categorical
element" is an inter-rater reliability problem. For complete nominal data,
Fleiss' kappa is standard; when readers cover different material (missing
cells), Krippendorff's alpha is preferred. The Census's cold readers enter by
different doors and cover different files, so alpha is the eventual target;
the dependency-free Fleiss' kappa below is the starting point.
"""

from __future__ import annotations

from collections.abc import Sequence


def convergence_ratio(agreements: int, total: int) -> float:
    """Fraction of readers that independently surfaced one element."""
    if total <= 0:
        raise ValueError("total must be positive")
    return agreements / total


def is_load_bearing_door(convergence: float, threshold: float = 0.5) -> bool:
    """Whether an entry door reliably led readers to the shared core."""
    return convergence >= threshold


def fleiss_kappa(table: Sequence[Sequence[int]]) -> float:
    """Fleiss' kappa for items rated by a fixed number of raters into k categories.

    ``table[i][j]`` = number of raters who placed item *i* in category *j*.
    Pure-Python, no dependencies. For uneven coverage or missing ratings,
    prefer Krippendorff's alpha (see the module docstring).
    """
    n_items = len(table)
    if n_items == 0:
        raise ValueError("table must have at least one item")
    n_raters = sum(table[0])
    if n_raters <= 1:
        raise ValueError("need at least two raters per item")
    if any(sum(row) != n_raters for row in table):
        raise ValueError("every item must have the same number of ratings")

    n_categories = len(table[0])
    p_item = [
        (sum(count * count for count in row) - n_raters) / (n_raters * (n_raters - 1))
        for row in table
    ]
    p_bar = sum(p_item) / n_items
    grand = n_items * n_raters
    p_category = [sum(row[j] for row in table) / grand for j in range(n_categories)]
    p_expected = sum(p * p for p in p_category)
    if p_expected == 1.0:
        return 1.0
    return (p_bar - p_expected) / (1 - p_expected)


if __name__ == "__main__":
    sample = convergence_ratio(9, 13)
    print(f"convergence={sample:.2f} load_bearing={is_load_bearing_door(sample)}")
    demo = [[11, 2], [3, 10]]  # 2 items, 13 raters, 2 categories
    print(f"fleiss_kappa={fleiss_kappa(demo):.3f}")
