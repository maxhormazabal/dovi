import pytest

from dovi.datamodel.base_models import InputFormat, guess_input_format
from dovi.datamodel.document import DoviDocument, TableItem, TextItem
from dovi.datamodel.pipeline_options import GenerationOptions, ReplicationOptions


def _sample_document() -> DoviDocument:
    return DoviDocument(
        name="invoice-0001",
        items=[
            TextItem(label="title", text="Invoice INV-0001"),
            TextItem(label="section_header", text="Line items"),
            TableItem(header=["Item", "Qty", "Price"], rows=[["Design work", "12", "960.00"]]),
            TextItem(text="Payment due within 30 days."),
        ],
    )


def test_export_to_markdown():
    md = _sample_document().export_to_markdown()
    assert md.startswith("# Invoice INV-0001")
    assert "## Line items" in md
    assert "| Item | Qty | Price |" in md
    assert "| Design work | 12 | 960.00 |" in md


def test_json_roundtrip(tmp_path):
    doc = _sample_document()
    path = doc.save_as_json(tmp_path / "doc.json")
    loaded = DoviDocument.load_from_json(path)
    assert loaded == doc
    assert isinstance(loaded.items[2], TableItem)


@pytest.mark.parametrize(
    ("filename", "expected"),
    [("a.pdf", InputFormat.PDF), ("b.DOCX", InputFormat.DOCX), ("c.jpeg", InputFormat.IMAGE)],
)
def test_guess_input_format(filename, expected):
    assert guess_input_format(filename) is expected


def test_guess_input_format_rejects_unknown():
    with pytest.raises(ValueError):
        guess_input_format("archive.zip")


def test_option_validation():
    with pytest.raises(ValueError):
        GenerationOptions(num_pages=0)
    with pytest.raises(ValueError):
        ReplicationOptions(layout_jitter=1.5)
