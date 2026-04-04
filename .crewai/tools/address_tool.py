#!/usr/bin/env python3
"""
CrewAI Tool: Address Space Writer

Writes crew state and entity references to the vault's content-addressable
memory system (the 19,533 stub files):
  NUMBERS (0-999) = Crew state memory (neurons)
  LETTERS (A-ZZZ) = Entity nodes

LINUX }!{ — targets Linux-native execution.
"""

from datetime import datetime, timezone
from pathlib import Path

from crewai.tools import BaseTool
from pydantic import Field


class AddressSpaceTool(BaseTool):
    name: str = "address_space_writer"
    description: str = (
        "Writes crew state or entity references to the vault's address space. "
        "Number addresses (e.g. '100') are crew state neurons. "
        "Letter addresses (e.g. 'JFAC', 'Idaho') are entity nodes. "
        "Provide the address (filename without .md) and the content to write."
    )
    vault_root: str = Field(default="")

    def _get_vault_root(self) -> Path:
        if self.vault_root:
            return Path(self.vault_root)
        return Path(__file__).resolve().parent.parent.parent

    def _run(self, address: str, content: str = "") -> str:
        """Write content to an address stub in the vault.

        Args:
            address: The stub filename without .md (e.g. '100', 'JFAC', 'Idaho')
            content: The content to write. Will be appended with frontmatter
                     if the file is currently empty.
        """
        root = self._get_vault_root()
        target = root / f"{address}.md"

        if not target.exists():
            return f"Error: Address '{address}.md' does not exist in the vault."

        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        current = target.read_text(encoding="utf-8")

        if len(current.strip()) == 0:
            # Empty stub — initialize with frontmatter + content
            new_content = f"""---
title: "{address}"
date created: "{now[:10]}"
authority: crewai
doc_class: neuron
---

# {address}

## Crew References

{content}

---
*Last updated by CrewAI address_space_writer at {now}*
"""
        else:
            # Existing content — append a crew reference section
            new_content = current.rstrip() + f"""

## Crew Reference — {now[:10]}

{content}

---
*Updated by CrewAI address_space_writer at {now}*
"""

        target.write_text(new_content, encoding="utf-8")
        return f"Written to {address}.md ({len(new_content)} bytes)"
