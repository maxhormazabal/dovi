from dovi.datamodel.base_models import OutputFormat, TaskStatus
from dovi.datamodel.pipeline_options import ContentStrategy, ReplicationOptions
from dovi.document_replicator import DocumentReplicator


def test_replicate_markdown_preserve(tmp_path):
    source = tmp_path / "memo.md"
    source.write_text("# Memo\n\n## Scope\n\nQuarterly review of supplier contracts.\n")

    options = ReplicationOptions(
        content_strategy=ContentStrategy.PRESERVE, output_format=OutputFormat.MD
    )
    result = DocumentReplicator(options).replicate(
        source, num_variants=3, output_dir=tmp_path / "out"
    )

    assert result.status is TaskStatus.SUCCESS
    assert [d.name for d in result.documents] == ["memo_0000", "memo_0001", "memo_0002"]
    assert len(result.artifacts) == 3
    assert all(a.path.exists() for a in result.artifacts)
