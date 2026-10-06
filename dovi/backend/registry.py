from __future__ import annotations

from dovi.backend.abstract_backend import AbstractRenderBackend
from dovi.backend.docx_backend import DocxRenderBackend
from dovi.backend.html_backend import HTMLRenderBackend
from dovi.backend.pdf_backend import WeasyPrintPdfBackend
from dovi.backend.text_backends import JsonRenderBackend, MarkdownRenderBackend
from dovi.datamodel.base_models import OutputFormat

_DEFAULT_BACKENDS: dict[OutputFormat, type[AbstractRenderBackend]] = {
    OutputFormat.PDF: WeasyPrintPdfBackend,
    OutputFormat.DOCX: DocxRenderBackend,
    OutputFormat.HTML: HTMLRenderBackend,
    OutputFormat.MD: MarkdownRenderBackend,
    OutputFormat.JSON: JsonRenderBackend,
}


def get_render_backend(output_format: OutputFormat) -> AbstractRenderBackend:
    try:
        backend_cls = _DEFAULT_BACKENDS[output_format]
    except KeyError:
        raise ValueError(f"No render backend registered for '{output_format.value}'") from None
    return backend_cls()


def register_render_backend(
    output_format: OutputFormat, backend_cls: type[AbstractRenderBackend]
) -> None:
    _DEFAULT_BACKENDS[output_format] = backend_cls
