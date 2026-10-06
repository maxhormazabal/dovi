from __future__ import annotations

import logging
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any

from dovi.datamodel.base_models import DocumentType, OutputFormat
from dovi.datamodel.pipeline_options import GenerationOptions
from dovi.datamodel.results import GenerationResult
from dovi.pipeline.generation_pipeline import StandardGenerationPipeline
from dovi.utils.slugify import slugify

_log = logging.getLogger(__name__)


class DocumentGenerator:
    """Generate new documents from a natural-language description.

    Example:
        >>> from dovi.document_generator import DocumentGenerator
        >>> generator = DocumentGenerator()
        >>> result = generator.generate("Invoice from a Barcelona design studio, 6 line items")
        >>> print(result.document.export_to_markdown())
    """

    def __init__(
        self,
        options: GenerationOptions | None = None,
        *,
        document_type: DocumentType | None = None,
        output_format: OutputFormat | None = None,
    ) -> None:
        options = options or GenerationOptions()
        overrides: dict[str, Any] = {}
        if document_type is not None:
            overrides["document_type"] = document_type
        if output_format is not None:
            overrides["output_format"] = output_format
        self.options = options.model_copy(update=overrides)
        self._pipeline = StandardGenerationPipeline(self.options)

    def generate(
        self,
        prompt: str,
        *,
        name: str | None = None,
        output_dir: str | Path | None = None,
    ) -> GenerationResult:
        name = name or slugify(prompt, max_length=48)
        _log.info("Generating %s (%s)", name, self.options.document_type.value)
        return self._pipeline.execute(
            prompt, name=name, output_dir=Path(output_dir) if output_dir else None
        )

    def generate_all(
        self, prompts: Iterable[str], *, output_dir: str | Path | None = None
    ) -> Iterator[GenerationResult]:
        for prompt in prompts:
            yield self.generate(prompt, output_dir=output_dir)
