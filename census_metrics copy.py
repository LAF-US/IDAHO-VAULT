"""Spelunking Census — convergence metrics (Hyperagent guest run).

Grown from the disposable machinery-test seed
(`_machinery_test_hyperagent_2026-06-25.py`), which carried
``convergence_ratio`` / ``is_load_bearing_door`` / ``fleiss_kappa`` and a
research note flagging Krippendorff's alpha as the eventual target. This module
keeps those and adds the set-valued machinery the Boids-refined design needs:

  - Boids mapping [mapping]: Cohesion <- entity-set agreement; Alignment <-
    heading agreement; Separation <- coverage-conditioned positional spread.
    (Reynolds 1986/87, https://red3d.com/cwr/boids/.)
  - Set agreement [research]: MASI = Jaccard x monotonicity (Passonneau 2006,
    LREC), usable as the distance delta inside Krippendorff's alpha for
    set-valued cells.

Status: apocrypha, not canon, safe to delete. Importing has no side effects;
the demo runs only under ``__main__``. ``krippendorff_alpha`` is a
dependency-free REFERENCE implementation: it is sanity-checked on
perfect/degenerate cases below, but cross-validate against Krippendorff (2004)
or a maintained package before any inferential use. n=13 readers is small, so
treat every alpha as an exploratory compass bearing, not a p-value.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Hashable, Sequence
from itertools import combinations


# --- seed functions (from the machinery-test module) -----------------------

def convergence_ratio(agreements: int, total: int) -> float:
    """Fraction of readers that independently surfaced one element."""
    if total <= 0:
        raise ValueError("total must be positive")
    if not 0 <= agreements <= total:
        raise ValueError("agreements must be between 0 and total")
    return agreements / total


def is_load_bearing_door(convergence: float, threshold: float = 0.5) -> bool:
    """Whether an entry door reliably led readers to the shared core."""
    return convergence >= threshold


def fleiss_kappa(table: Sequence[Sequence[int]]) -> float:
    """Fleiss' kappa for items rated by a fixed number of raters into k categories.

    ``table[i][j]`` = number of raters who placed item *i* in category *j*. For
    uneven coverage or missing ratings, prefer ``krippendorff_alpha`` (the
    realistic Census case, since cold readers enter by different doors).
    """
    n_items = len(table)
    if n_items == 0:
        raise ValueError("table must have at least one item")
    n_categories = len(table[0])
    if n_categories == 0:
        raise ValueError("each item must have at least one category")
    if any(len(row) != n_categories for row in table):
        raise ValueError("every item must have the same number of categories")
    if any(type(c) is not int or c < 0 for row in table for c in row):
        raise ValueError("counts must be non-negative integers")
    n_raters = sum(table[0])
    if n_raters <= 1:
        raise ValueError("need at least two raters per item")
    if any(sum(row) != n_raters for row in table):
        raise ValueError("every item must have the same number of ratings")
    p_item = [
        (sum(c * c for c in row) - n_raters) / (n_raters * (n_raters - 1))
        for row in table
    ]
    p_bar = sum(p_item) / n_items
    grand = n_items * n_raters
    p_cat = [sum(row[j] for row in table) / grand for j in range(n_categories)]
    p_exp = sum(p * p for p in p_cat)
    if math.isclose(p_exp, 1.0):
        return 1.0  # perfect expected agreement: kappa undefined; report 1.0
    return (p_bar - p_exp) / (1 - p_exp)


# --- set agreement: Jaccard and MASI (Passonneau 2006) ---------------------

def jaccard(a: set, b: set) -> float:
    """len(A & B) / len(A | B) (intersection over union). Two empty sets count as identical (1.0)."""
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def _monotonicity(a: set, b: set) -> float:
    """MASI's M term: 1 identical, 2/3 subset, 1/3 overlapping, 0 disjoint."""
    if a == b:
        return 1.0
    if not (a & b):
        return 0.0
    if a < b or b < a:
        return 2.0 / 3.0
    return 1.0 / 3.0


def masi(a: set, b: set) -> float:
    """MASI set similarity = Jaccard x monotonicity (Passonneau 2006). Range [0,1]."""
    if not a and not b:
        return 1.0
    return jaccard(a, b) * _monotonicity(a, b)


def masi_distance(a: set, b: set) -> float:
    """1 - MASI; a distance in [0,1] usable as Krippendorff's delta for set cells."""
    return 1.0 - masi(a, b)


# --- Krippendorff's alpha (reference impl; pluggable distance) --------------

def nominal_distance(x: Hashable, y: Hashable) -> float:
    """0 if equal, else 1 — the nominal metric."""
    return 0.0 if x == y else 1.0


def krippendorff_alpha(
    reliability_data: Sequence[Sequence[object]],
    distance: Callable[[object, object], float] = nominal_distance,
) -> float:
    """Krippendorff's alpha for m coders x N units, with missing values as None.

    ``reliability_data[c][u]`` = coder *c*'s value for unit *u*, or ``None`` if
    uncoded. ``distance`` is any metric delta(x, y) >= 0 with delta(x, x) = 0
    (e.g. ``nominal_distance``, or ``masi_distance`` for set-valued cells).

    alpha = 1 - D_o / D_e over the coincidence of all value pairs that share a
    unit, with the standard 1/(m_u - 1) pairing correction. Units with fewer
    than two values are dropped. Returns 1.0 when D_e == 0 (no observable
    disagreement is possible).

    REFERENCE IMPLEMENTATION — sanity-checked on perfect/degenerate cases only;
    cross-validate against Krippendorff (2004) before inferential use.
    """
    if len(reliability_data) < 2:
        raise ValueError("need at least two coders")
    n_units = max((len(row) for row in reliability_data), default=0)

    units: list[list[object]] = []
    for u in range(n_units):
        vals = [row[u] for row in reliability_data
                if u < len(row) and row[u] is not None]
        if len(vals) >= 2:
            units.append(vals)
    if not units:
        raise ValueError("no unit has two or more values")

    total_pairable = sum(len(v) for v in units)
    d_o = 0.0
    for vals in units:
        m_u = len(vals)
        pair_sum = sum(distance(a, b) for a, b in combinations(vals, 2))
        d_o += (2.0 / (m_u - 1)) * pair_sum
    d_o /= total_pairable

    pooled = [v for vals in units for v in vals]
    n = len(pooled)
    d_e = sum(distance(a, b) for a, b in combinations(pooled, 2)) * 2.0 / (n * (n - 1))

    if math.isclose(d_e, 0.0):
        return 1.0
    return 1.0 - d_o / d_e


def _demo() -> None:
    """Print examples and run analytically-certain sanity checks (under __main__)."""
    cr = convergence_ratio(9, 13)
    print(f"convergence={cr:.2f} load_bearing={is_load_bearing_door(cr)}")
    print(f"fleiss_kappa={fleiss_kappa([[11, 2], [3, 10]]):.3f}")

    # MASI: hand-verifiable from Passonneau (2006).
    assert masi({1, 2, 3}, {1, 2, 3}) == 1.0
    assert math.isclose(masi({1, 2}, {1, 2, 3}), (2 / 3) * (2 / 3))  # subset
    assert masi({1}, {2}) == 0.0
    print("masi sanity: ok")

    # alpha: perfect within-unit agreement -> 1.0 (nominal and set-valued).
    assert math.isclose(krippendorff_alpha([["a", "b", "c"], ["a", "b", "c"]]), 1.0)
    assert math.isclose(
        krippendorff_alpha([[{1, 2}, {3}], [{1, 2}, {3}]], distance=masi_distance),
        1.0,
    )
    # total disagreement on a 2x1-style nominal case -> alpha <= 0.
    assert krippendorff_alpha([["a", "b"], ["b", "a"]]) <= 0.0
    print("alpha sanity: ok")


if __name__ == "__main__":
    _demo()
