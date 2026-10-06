from __future__ import annotations

from pathlib import Path

from dovi.datamodel.base_models import DoviComponentType, ErrorItem, TaskStatus
from dovi.datamodel.pipeline_options import GenerationOptions
from dovi.datamodel.results import GenerationResult
from dovi.models.content_synthesizer import ContentSynthesizer
from dovi.models.layout_planner import LayoutPlanner
from dovi.pipeline.base_pipeline import BasePipeline
from dovi.utils.profiling import time_recorder


class StandardGenerationPipeline(BasePipeline):
    """plan -> synthesize -> render"""

    options: GenerationOptions

    def __init__(self, options: GenerationOptions) -> None:
        super().__init__(options)
        self.planner = LayoutPlanner(options)
        self.synthesizer = ContentSynthesizer(options)

    def execute(self, prompt: str, name: str, output_dir: Path | None) -> GenerationResult:
        result = GenerationResult(status=TaskStatus.STARTED)
        with time_recorder(result.timings, "plan"):
            plan = self.planner.plan(prompt)
        try:
            with time_recorder(result.timings, "synthesize"):
                result.document = self.synthesizer.synthesize(prompt, plan, name)
        except Exception as exc:
            result.errors.append(
                ErrorItem(
                    component_type=DoviComponentType.SYNTHESIZER,
                    module_name=type(self.synthesizer).__name__,
                    error_message=str(exc),
                )
            )
            result.status = TaskStatus.FAILURE
            return result

        with time_recorder(result.timings, "render"):
            artifact = self._render(result.document, output_dir, result.errors)
        if artifact is not None:
            result.artifacts.append(artifact)
        result.status = TaskStatus.PARTIAL_SUCCESS if result.errors else TaskStatus.SUCCESS
        return result
