from __future__ import annotations

from html import escape
from pathlib import Path

from dovi.backend.abstract_backend import AbstractRenderBackend
from dovi.datamodel.base_models import OutputFormat
from dovi.datamodel.document import DoviDocument, PictureItem, TableItem, TextItem
from dovi.datamodel.results import RenderedArtifact

_BASE_CSS = """
@page { size: A4; margin: 18mm 16mm; }
body { font-family: "Helvetica Neue", Arial, sans-serif; font-size: 10.5pt; color: #1b1f24; }
h1 { font-size: 20pt; margin: 0 0 12pt; }
h2 { font-size: 13pt; margin: 14pt 0 6pt; }
h3 { font-size: 11pt; margin: 10pt 0 4pt; }
table { width: 100%; border-collapse: collapse; margin: 8pt 0; }
th, td { border: 0.5pt solid #9aa4b2; padding: 4pt 6pt; text-align: left; }
th { background: #eef1f5; }
figure { margin: 8pt 0; }
figcaption, .caption { font-size: 9pt; color: #5a6472; }
.footnote { font-size: 8pt; color: #5a6472; }
.page { page-break-after: always; }
.page:last-child { page-break-after: auto; }
"""


def render_html(document: DoviDocument) -> str:
    pages: list[str] = []
    for page in document.pages:
        parts: list[str] = []
        for item in document.iterate_items(page.page_no):
            if isinstance(item, TextItem):
                text = escape(item.text)
                if item.label == "title":
                    parts.append(f"<h1>{text}</h1>")
                elif item.label == "section_header":
                    level = min(item.level + 1, 6)
                    parts.append(f"<h{level}>{text}</h{level}>")
                elif item.label in ("caption", "footnote"):
                    parts.append(f'<p class="{item.label}">{text}</p>')
                else:
                    parts.append(f"<p>{text}</p>")
            elif isinstance(item, TableItem):
                head = "".join(f"<th>{escape(c)}</th>" for c in item.header)
                body = "".join(
                    "<tr>" + "".join(f"<td>{escape(c)}</td>" for c in row) + "</tr>"
                    for row in item.rows
                )
                thead = f"<thead><tr>{head}</tr></thead>" if head else ""
                parts.append(f"<table>{thead}<tbody>{body}</tbody></table>")
            elif isinstance(item, PictureItem):
                caption = f"<figcaption>{escape(item.caption)}</figcaption>" if item.caption else ""
                src = escape(item.uri or "")
                parts.append(f'<figure><img src="{src}" alt="">{caption}</figure>')
        pages.append(f'<section class="page" data-page="{page.page_no}">{"".join(parts)}</section>')

    lang = escape(document.metadata.language)
    title = escape(document.name)
    return (
        f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8">'
        f"<title>{title}</title><style>{_BASE_CSS}</style></head>"
        f"<body>{''.join(pages)}</body></html>"
    )


class HTMLRenderBackend(AbstractRenderBackend):
    output_format = OutputFormat.HTML
    media_type = "text/html"
    extension = "html"

    def render(self, document: DoviDocument, output_path: Path) -> RenderedArtifact:
        output_path.write_text(render_html(document), encoding="utf-8")
        return self._artifact(output_path)
