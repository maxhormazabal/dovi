from __future__ import annotations

from pydantic import BaseModel, Field

from dovi.datamodel.base_models import DocumentType
from dovi.datamodel.pipeline_options import GenerationOptions

# Section skeletons used to seed the planner for well-known document types.
_SECTION_TEMPLATES: dict[DocumentType, list[str]] = {
    DocumentType.INVOICE: ["header", "parties", "line_items", "totals", "payment_terms"],
    DocumentType.RECEIPT: ["merchant", "line_items", "totals", "footer"],
    DocumentType.FORM: ["title", "instructions", "fields", "signature"],
    DocumentType.LETTER: ["letterhead", "recipient", "body", "closing"],
    DocumentType.REPORT: ["title", "summary", "sections", "tables", "conclusion"],
    DocumentType.CONTRACT: ["title", "parties", "recitals", "clauses", "signatures"],
    DocumentType.ID_CARD: ["issuer", "holder", "fields", "machine_readable_zone"],
    DocumentType.BANK_STATEMENT: ["header", "account", "transactions", "balance"],
    DocumentType.GENERIC: ["title", "body"],
}


class SectionSlot(BaseModel):
    name: str
    page_no: int
    expects_table: bool = False


class LayoutPlan(BaseModel):
    document_type: DocumentType
    num_pages: int
    slots: list[SectionSlot] = Field(default_factory=list)


class LayoutPlanner:
    """Distributes the logical sections of a document type across pages."""

    def __init__(self, options: GenerationOptions) -> None:
        self.options = options

    def plan(self, prompt: str) -> LayoutPlan:
        sections = _SECTION_TEMPLATES[self.options.document_type]
        num_pages = self.options.num_pages
        per_page = max(1, -(-len(sections) // num_pages))
        slots = [
            SectionSlot(
                name=name,
                page_no=min(idx // per_page + 1, num_pages),
                expects_table=self.options.include_tables
                and name in {"line_items", "transactions", "tables", "fields"},
            )
            for idx, name in enumerate(sections)
        ]
        return LayoutPlan(
            document_type=self.options.document_type, num_pages=num_pages, slots=slots
        )
