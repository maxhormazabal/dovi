from __future__ import annotations

import random

from dovi.datamodel.document import BoundingBox, DoviDocument
from dovi.datamodel.pipeline_options import ContentStrategy, ReplicationOptions


class VariantSampler:
    """Produces new documents that share the layout of a source document."""

    def __init__(self, options: ReplicationOptions) -> None:
        self.options = options
        self._rng = random.Random(options.seed)

    def sample(self, source: DoviDocument, index: int) -> DoviDocument:
        variant = source.model_copy(deep=True)
        variant.name = f"{source.name}_{index:04d}"
        variant.metadata.source = source.metadata.source or source.name
        variant.metadata.seed = self.options.seed

        if self.options.layout_jitter > 0:
            for item in variant.items:
                if item.bbox is not None:
                    item.bbox = self._jitter(item.bbox)

        if self.options.content_strategy is ContentStrategy.PRESERVE:
            return variant
        raise NotImplementedError(
            f"Content strategy '{self.options.content_strategy.value}' is not available in this "
            "release."
        )

    def _jitter(self, bbox: BoundingBox) -> BoundingBox:
        dx = self._rng.uniform(-1, 1) * self.options.layout_jitter * bbox.width * 0.1
        dy = self._rng.uniform(-1, 1) * self.options.layout_jitter * bbox.height * 0.1
        return BoundingBox(
            left=bbox.left + dx, top=bbox.top + dy, right=bbox.right + dx, bottom=bbox.bottom + dy
        )
