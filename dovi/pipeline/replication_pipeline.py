from __future__ import annotations

from pathlib import Path

from dovi.datamodel.base_models import DoviComponentType, ErrorItem, TaskStatus
from dovi.datamodel.pipeline_options import ReplicationOptions
from dovi.datamodel.results import ReplicationResult
from dovi.models.layout_analyzer import LayoutAnalyzer
from dovi.models.variant_sampler import VariantSampler
from dovi.pipeline.base_pipeline import BasePipeline
from dovi.utils.profiling import time_recorder


class StandardReplicationPipeline(BasePipeline):
    """analyze -> sample variants -> render"""

    options: ReplicationOptions

    def __init__(self, options: ReplicationOptions) -> None:
        super().__init__(options)
        self.analyzer = LayoutAnalyzer()
        self.sampler = VariantSampler(options)

    def execute(self, source: Path, output_dir: Path | None) -> ReplicationResult:
        result = ReplicationResult(status=TaskStatus.STARTED, source=source)
        try:
            with time_recorder(result.timings, "analyze"):
                result.source_document = self.analyzer.analyze(source)
        except Exception as exc:
            result.errors.append(
                ErrorItem(
                    component_type=DoviComponentType.ANALYZER,
                    module_name=type(self.analyzer).__name__,
                    error_message=str(exc),
                )
            )
            result.status = TaskStatus.FAILURE
            return result

        for index in range(self.options.num_variants):
            try:
                with time_recorder(result.timings, "sample"):
                    variant = self.sampler.sample(result.source_document, index)
            except Exception as exc:
                result.errors.append(
                    ErrorItem(
                        component_type=DoviComponentType.SYNTHESIZER,
                        module_name=type(self.sampler).__name__,
                        error_message=str(exc),
                    )
                )
                break
            result.documents.append(variant)
            with time_recorder(result.timings, "render"):
                artifact = self._render(variant, output_dir, result.errors)
            if artifact is not None:
                result.artifacts.append(artifact)

        if not result.documents:
            result.status = TaskStatus.FAILURE
        elif result.errors:
            result.status = TaskStatus.PARTIAL_SUCCESS
        else:
            result.status = TaskStatus.SUCCESS
        return result
