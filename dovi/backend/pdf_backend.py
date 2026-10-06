from __future__ import annotations

import importlib.util
from pathlib import Path

from dovi.backend.abstract_backend import AbstractRenderBackend
from dovi.backend.html_backend import render_html
from dovi.datamodel.base_models import OutputFormat
from dovi.datamodel.document import DoviDocument
from dovi.datamodel.results import RenderedArtifact
from dovi.exceptions import BackendNotAvailableError


class WeasyPrintPdfBackend(AbstractRenderBackend):
    output_format = OutputFormat.PDF
    media_type = "application/pdf"
    extension = "pdf"

    @classmethod
    def is_available(cls) -> bool:
        return importlib.util.find_spec("weasyprint") is not None

    def render(self, document: DoviDocument, output_path: Path) -> RenderedArtifact:
        if not self.is_available():
            raise BackendNotAvailableError("pdf", extra="pdf")

        from weasyprint import HTML

        HTML(string=render_html(document)).write_pdf(str(output_path))
        return self._artifact(output_path)
