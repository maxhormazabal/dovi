from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field

from dovi.datamodel.base_models import DocumentType


class BoundingBox(BaseModel):
    """Bounding box in page coordinates (points, top-left origin)."""

    left: float
    top: float
    right: float
    bottom: float

    @property
    def width(self) -> float:
        return self.right - self.left

    @property
    def height(self) -> float:
        return self.bottom - self.top


class Size(BaseModel):
    width: float = 595.0
    height: float = 842.0


class _BaseItem(BaseModel):
    page_no: int = 1
    bbox: BoundingBox | None = None


class TextItem(_BaseItem):
    kind: Literal["text"] = "text"
    label: Literal["title", "section_header", "paragraph", "caption", "footnote", "key_value"] = (
        "paragraph"
    )
    text: str
    level: int = 1


class TableItem(_BaseItem):
    kind: Literal["table"] = "table"
    header: list[str] = Field(default_factory=list)
    rows: list[list[str]] = Field(default_factory=list)


class PictureItem(_BaseItem):
    kind: Literal["picture"] = "picture"
    uri: str | None = None
    caption: str | None = None


DocItem = Annotated[TextItem | TableItem | PictureItem, Field(discriminator="kind")]


class PageItem(BaseModel):
    page_no: int
    size: Size = Field(default_factory=Size)


class DocumentMetadata(BaseModel):
    document_type: DocumentType = DocumentType.GENERIC
    language: str = "en"
    source: str | None = None
    seed: int | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class DoviDocument(BaseModel):
    """Format-agnostic representation of a generated or replicated document."""

    name: str
    metadata: DocumentMetadata = Field(default_factory=DocumentMetadata)
    pages: list[PageItem] = Field(default_factory=lambda: [PageItem(page_no=1)])
    items: list[DocItem] = Field(default_factory=list)

    @property
    def num_pages(self) -> int:
        return len(self.pages)

    def iterate_items(self, page_no: int | None = None) -> list[DocItem]:
        if page_no is None:
            return list(self.items)
        return [item for item in self.items if item.page_no == page_no]

    def export_to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")

    def export_to_json(self, indent: int = 2) -> str:
        return json.dumps(self.export_to_dict(), indent=indent, ensure_ascii=False)

    def export_to_markdown(self) -> str:
        blocks: list[str] = []
        for item in self.items:
            if isinstance(item, TextItem):
                if item.label == "title":
                    blocks.append(f"# {item.text}")
                elif item.label == "section_header":
                    blocks.append(f"{'#' * min(item.level + 1, 6)} {item.text}")
                elif item.label == "caption":
                    blocks.append(f"*{item.text}*")
                else:
                    blocks.append(item.text)
            elif isinstance(item, TableItem):
                blocks.append(_table_to_markdown(item))
            elif isinstance(item, PictureItem):
                alt = item.caption or "picture"
                blocks.append(f"![{alt}]({item.uri or ''})")
        return "\n\n".join(blocks) + ("\n" if blocks else "")

    def save_as_json(self, path: str | Path) -> Path:
        path = Path(path)
        path.write_text(self.export_to_json(), encoding="utf-8")
        return path

    def save_as_markdown(self, path: str | Path) -> Path:
        path = Path(path)
        path.write_text(self.export_to_markdown(), encoding="utf-8")
        return path

    @classmethod
    def load_from_json(cls, path: str | Path) -> DoviDocument:
        return cls.model_validate_json(Path(path).read_text(encoding="utf-8"))


def _table_to_markdown(table: TableItem) -> str:
    n_cols = max([len(table.header), *(len(r) for r in table.rows)], default=0)
    if n_cols == 0:
        return ""
    header = table.header or [""] * n_cols
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(["---"] * n_cols) + " |",
    ]
    for row in table.rows:
        padded = row + [""] * (n_cols - len(row))
        lines.append("| " + " | ".join(padded) + " |")
    return "\n".join(lines)
