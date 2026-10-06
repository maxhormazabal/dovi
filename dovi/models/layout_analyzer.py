from __future__ import annotations

from pathlib import Path

from dovi.datamodel.base_models import InputFormat, guess_input_format
from dovi.datamodel.document import DocumentMetadata, DoviDocument, TextItem


class LayoutAnalyzer:
    """Recovers the structure (pages, regions, reading order) of a source document."""

    def analyze(self, source: Path) -> DoviDocument:
        if source.suffix.lower() == ".json":
            return DoviDocument.load_from_json(source)

        fmt = guess_input_format(source)
        if fmt is InputFormat.MD:
            return self._from_markdown(source)
        raise NotImplementedError(
            f"Layout analysis for '{fmt.value}' inputs is not available in this release."
        )

    @staticmethod
    def _from_markdown(source: Path) -> DoviDocument:
        items = []
        for block in source.read_text(encoding="utf-8").split("\n\n"):
            block = block.strip()
            if not block:
                continue
            if block.startswith("# "):
                items.append(TextItem(label="title", text=block[2:].strip()))
            elif block.startswith("#"):
                level = len(block) - len(block.lstrip("#"))
                items.append(
                    TextItem(
                        label="section_header", text=block.lstrip("#").strip(), level=level - 1
                    )
                )
            else:
                items.append(TextItem(text=block))
        return DoviDocument(
            name=source.stem, metadata=DocumentMetadata(source=str(source)), items=items
        )
