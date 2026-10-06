from __future__ import annotations

from enum import Enum
from pathlib import Path

from pydantic import BaseModel


class InputFormat(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    IMAGE = "image"
    HTML = "html"
    MD = "md"


class OutputFormat(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    HTML = "html"
    MD = "md"
    JSON = "json"
    PNG = "png"


class DocumentType(str, Enum):
    INVOICE = "invoice"
    RECEIPT = "receipt"
    FORM = "form"
    LETTER = "letter"
    REPORT = "report"
    CONTRACT = "contract"
    ID_CARD = "id_card"
    BANK_STATEMENT = "bank_statement"
    GENERIC = "generic"


class TaskStatus(str, Enum):
    PENDING = "pending"
    STARTED = "started"
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILURE = "failure"


class DoviComponentType(str, Enum):
    PLANNER = "planner"
    SYNTHESIZER = "synthesizer"
    RENDERER = "renderer"
    ANALYZER = "analyzer"


class ErrorItem(BaseModel):
    component_type: DoviComponentType
    module_name: str
    error_message: str


FORMAT_EXTENSIONS: dict[InputFormat, list[str]] = {
    InputFormat.PDF: ["pdf"],
    InputFormat.DOCX: ["docx", "dotx"],
    InputFormat.IMAGE: ["png", "jpg", "jpeg", "tif", "tiff", "bmp", "webp"],
    InputFormat.HTML: ["html", "htm"],
    InputFormat.MD: ["md", "markdown"],
}


def guess_input_format(path: str | Path) -> InputFormat:
    suffix = Path(path).suffix.lower().lstrip(".")
    for fmt, extensions in FORMAT_EXTENSIONS.items():
        if suffix in extensions:
            return fmt
    raise ValueError(f"Unsupported input file extension: '.{suffix}'")
