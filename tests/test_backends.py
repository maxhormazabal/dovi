from dovi.backend.registry import get_render_backend
from dovi.datamodel.base_models import OutputFormat
from dovi.datamodel.document import DoviDocument, TextItem


def test_html_backend(tmp_path):
    doc = DoviDocument(name="letter", items=[TextItem(label="title", text="Dear <Client>")])
    backend = get_render_backend(OutputFormat.HTML)
    artifact = backend.render(doc, tmp_path / "letter.html")
    html = artifact.path.read_text()
    assert artifact.media_type == "text/html"
    assert "<h1>Dear &lt;Client&gt;</h1>" in html


def test_markdown_backend(tmp_path):
    doc = DoviDocument(name="note", items=[TextItem(text="Hello")])
    artifact = get_render_backend(OutputFormat.MD).render(doc, tmp_path / "note.md")
    assert artifact.path.read_text() == "Hello\n"
