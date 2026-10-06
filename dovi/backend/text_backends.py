from __future__ import annotations

from pathlib import Path

from dovi.backend.abstract_backend import AbstractRenderBackend
from dovi.datamodel.base_models import OutputFormat
from dovi.datamodel.document import DoviDocument
from dovi.datamodel.results import RenderedArtifact


class MarkdownRenderBackend(AbstractRenderBackend):
    output_format = OutputFormat.MD
    media_type = "text/markdown"
    extension = "md"

    def render(self, document: DoviDocument, output_path: Path) -> RenderedArtifact:
        return self._artifact(document.save_as_markdown(output_path))


class JsonRenderBackend(AbstractRenderBackend):
    output_format = OutputFormat.JSON
    media_type = "application/json"
    extension = "json"

    def render(self, document: DoviDocument, output_path: Path) -> RenderedArtifact:
        return self._artifact(document.save_as_json(output_path))
