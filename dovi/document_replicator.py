from __future__ import annotations

import logging
from collections.abc import Iterable, Iterator
from pathlib import Path

from dovi.datamodel.pipeline_options import ReplicationOptions
from dovi.datamodel.results import ReplicationResult
from dovi.pipeline.replication_pipeline import StandardReplicationPipeline

_log = logging.getLogger(__name__)


class DocumentReplicator:
    """Create new documents that replicate the layout and style of an existing one.

    Example:
        >>> from dovi.document_replicator import DocumentReplicator
        >>> replicator = DocumentReplicator()
        >>> result = replicator.replicate("invoice.pdf", num_variants=10, output_dir="out/")
        >>> for doc in result.documents:
        ...     print(doc.name)
    """

    def __init__(self, options: ReplicationOptions | None = None) -> None:
        self.options = options or ReplicationOptions()

    def replicate(
        self,
        source: str | Path,
        *,
        num_variants: int | None = None,
        output_dir: str | Path | None = None,
    ) -> ReplicationResult:
        source = Path(source)
        if not source.exists():
            raise FileNotFoundError(source)

        options = self.options
        if num_variants is not None:
            options = options.model_copy(update={"num_variants": num_variants})

        _log.info("Replicating %s (%d variants)", source.name, options.num_variants)
        pipeline = StandardReplicationPipeline(options)
        return pipeline.execute(source, output_dir=Path(output_dir) if output_dir else None)

    def replicate_all(
        self, sources: Iterable[str | Path], *, output_dir: str | Path | None = None
    ) -> Iterator[ReplicationResult]:
        for source in sources:
            yield self.replicate(source, output_dir=output_dir)
