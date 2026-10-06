from __future__ import annotations

import json
from typing import Any

from dovi.datamodel.document import (
    DocItem,
    DocumentMetadata,
    DoviDocument,
    PageItem,
    TableItem,
    TextItem,
)
from dovi.datamodel.pipeline_options import GenerationOptions
from dovi.models.layout_planner import LayoutPlan
from dovi.models.llm_client import LLMClient

_SYSTEM_PROMPT = """\
You write realistic content for business and administrative documents.
Return a JSON object with a single key "sections". Each section has:
  "name": the slot name you were given,
  "heading": optional section heading,
  "paragraphs": list of strings,
  "table": optional object with "header" (list of strings) and "rows" (list of lists of strings).
Use the requested language. Values such as names, amounts and dates must be internally consistent.
"""


class ContentSynthesizer:
    """Fills a :class:`LayoutPlan` with text and tables produced by a language model."""

    def __init__(self, options: GenerationOptions, client: LLMClient | None = None) -> None:
        self.options = options
        self.client = client or LLMClient(options.model)

    def synthesize(self, prompt: str, plan: LayoutPlan, name: str) -> DoviDocument:
        request = {
            "instruction": prompt,
            "document_type": plan.document_type.value,
            "language": self.options.language,
            "slots": [slot.model_dump() for slot in plan.slots],
        }
        response = self.client.complete_json(_SYSTEM_PROMPT, json.dumps(request))
        return self._to_document(response, plan, name)

    def _to_document(self, response: dict[str, Any], plan: LayoutPlan, name: str) -> DoviDocument:
        page_of = {slot.name: slot.page_no for slot in plan.slots}
        items: list[DocItem] = [TextItem(label="title", text=name, page_no=1)]
        for section in response.get("sections", []):
            page_no = page_of.get(section.get("name", ""), 1)
            if heading := section.get("heading"):
                items.append(TextItem(label="section_header", text=heading, page_no=page_no))
            for paragraph in section.get("paragraphs", []):
                items.append(TextItem(text=paragraph, page_no=page_no))
            if table := section.get("table"):
                items.append(
                    TableItem(
                        header=table.get("header", []),
                        rows=table.get("rows", []),
                        page_no=page_no,
                    )
                )
        return DoviDocument(
            name=name,
            metadata=DocumentMetadata(
                document_type=plan.document_type,
                language=self.options.language,
                seed=self.options.seed,
            ),
            pages=[PageItem(page_no=i + 1) for i in range(plan.num_pages)],
            items=items,
        )
