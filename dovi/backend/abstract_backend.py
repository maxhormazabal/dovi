from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from dovi.datamodel.base_models import OutputFormat
from dovi.datamodel.document import DoviDocument
from dovi.datamodel.results import RenderedArtifact


class AbstractRenderBackend(ABC):
    """Turns a :class:`DoviDocument` into a concrete file format."""

    output_format: OutputFormat
    media_type: str
    extension: str

    @abstractmethod
    def render(self, document: DoviDocument, output_path: Path) -> RenderedArtifact: ...

    @classmethod
    def is_available(cls) -> bool:
        return True

    def _artifact(self, path: Path) -> RenderedArtifact:
        return RenderedArtifact(path=path, media_type=self.media_type)
