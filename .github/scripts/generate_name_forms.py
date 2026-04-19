"""
generate_name_forms.py — Bookbinding companion to plant_epithets.py.

Reads the EPITHETS dict and outputs all four grammatical forms for each name:
  base | possessive | plural | plural possessive

AP style for possessives: names ending in S take bare apostrophe (ZEUS'),
all others take 'S (ODIN'S).

Output: console table + optional markdown file.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Import EPITHETS from the sibling script without running its side effects.
# We replicate just the dict here to keep generate_name_forms independently runnable.
from plant_epithets import EPITHETS


def possessive(name: str) -> str:
    if name.endswith("S") or name.endswith("X") or name.endswith("Z"):
        return name + "'"
    return name + "'S"


def plural(name: str) -> str:
    if name.endswith("Y") and not name.endswith("-Y"):
        return name[:-1] + "IES"
    if name.endswith("S") or name.endswith("X") or name.endswith("Z"):
        return name + "ES"
    if "-" in name:
        return name + "S"
    return name + "S"


def plural_possessive(name: str) -> str:
    return plural(name) + "'"


def name_forms(name: str) -> dict:
    return {
        "base": name,
        "possessive": possessive(name),
        "plural": plural(name),
        "plural_possessive": plural_possessive(name),
    }


def print_table(rows: list[dict]) -> None:
    headers = ["BASE", "POSSESSIVE", "PLURAL", "PLURAL POSSESSIVE", "EPITHET"]
    widths = [
        max(len(h), max(len(r["base"]) for r in rows)) for h in headers[:1]
    ] + [
        max(len(h), max(len(r["possessive"]) for r in rows)),
        max(len(h), max(len(r["plural"]) for r in rows)),
        max(len(h), max(len(r["plural_possessive"]) for r in rows)),
        max(len(headers[4]), max(len(r["epithet"]) for r in rows)),
    ]

    sep = "+-" + "-+-".join("-" * w for w in widths) + "-+"
    header_row = "| " + " | ".join(h.ljust(w) for h, w in zip(headers, widths)) + " |"

    print(sep)
    print(header_row)
    print(sep)
    for r in rows:
        cells = [r["base"], r["possessive"], r["plural"], r["plural_possessive"], r["epithet"]]
        print("| " + " | ".join(c.ljust(w) for c, w in zip(cells, widths)) + " |")
    print(sep)


def to_markdown(rows: list[dict]) -> str:
    headers = ["BASE", "POSSESSIVE", "PLURAL", "PLURAL POSSESSIVE", "EPITHET"]
    lines = ["| " + " | ".join(headers) + " |"]
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for r in rows:
        lines.append(
            "| " + " | ".join([r["base"], r["possessive"], r["plural"], r["plural_possessive"], r["epithet"]]) + " |"
        )
    return "\n".join(lines)


def main() -> None:
    rows = []
    for name, epithet in sorted(EPITHETS.items()):
        forms = name_forms(name)
        forms["epithet"] = epithet
        rows.append(forms)

    if "--md" in sys.argv:
        vault = "C:/Users/loganf/Documents/IDAHO-VAULT"
        out_path = os.path.join(vault, "!", "NAME-FORMS-TABLE-2026-04-17.md")
        frontmatter = (
            "---\n"
            "authority: LOGAN\n"
            "related:\n"
            "  - BOOKS-OF-NAMES-AND-THE-PRESS-2026-04-17\n"
            "  - The world is quiet here\n"
            "date: 2026-04-17\n"
            "generated-by: .github/scripts/generate_name_forms.py\n"
            "---\n\n"
            "# Name Forms Table\n\n"
            "All four grammatical forms (AP possessive style) + epithet "
            "for every entry in the EPITHETS dict.\n\n"
        )
        md = frontmatter + to_markdown(rows)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"Written: {out_path}")
    else:
        print_table(rows)
        print(f"\n{len(rows)} names processed.")


if __name__ == "__main__":
    main()
