from __future__ import annotations

import logging
from pathlib import Path

from dovi.backend.registry import get_render_backend
from dovi.datamodel.base_models import DoviComponentType, ErrorItem
from dovi.datamodel.document import DoviDocument
from dovi.datamodel.pipeline_options import PipelineOptions
from dovi.datamodel.results import RenderedArtifact

_log = logging.getLogger(__name__)


class BasePipeline:
    def __init__(self, options: PipelineOptions) -> None:
        self.options = options
        self.render_backend = get_render_backend(options.output_format)

    def _render(
        self, document: DoviDocument, output_dir: Path | None, errors: list[ErrorItem]
    ) -> RenderedArtifact | None:
        if output_dir is None:
            return None
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / f"{document.name}.{self.render_backend.extension}"
        try:
            return self.render_backend.render(document, path)
        except Exception as exc:
            _log.warning("Rendering of %s failed: %s", document.name, exc)
            errors.append(
                ErrorItem(
                    component_type=DoviComponentType.RENDERER,
                    module_name=type(self.render_backend).__name__,
                    error_message=str(exc),
                )
            )
            return None
