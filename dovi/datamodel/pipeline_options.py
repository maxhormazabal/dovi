from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field, SecretStr

from dovi.datamodel.base_models import DocumentType, OutputFormat


class ModelProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"
    VLLM = "vllm"


class ModelOptions(BaseModel):
    """Configuration of the language/vision model used by the pipelines."""

    provider: ModelProvider = ModelProvider.OPENAI
    model_id: str = "gpt-4o-mini"
    api_key: SecretStr | None = None
    base_url: str | None = None
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4096, gt=0)
    timeout: float = Field(default=120.0, gt=0)


class LayoutStyle(str, Enum):
    MINIMAL = "minimal"
    CORPORATE = "corporate"
    ACADEMIC = "academic"
    FORM = "form"
    RANDOM = "random"


class PipelineOptions(BaseModel):
    output_format: OutputFormat = OutputFormat.PDF
    seed: int | None = None
    model: ModelOptions = Field(default_factory=ModelOptions)
    document_timeout: float | None = None


class GenerationOptions(PipelineOptions):
    """Options controlling document generation from a prompt or specification."""

    document_type: DocumentType = DocumentType.GENERIC
    language: str = "en"
    num_pages: int = Field(default=1, ge=1, le=50)
    layout_style: LayoutStyle = LayoutStyle.CORPORATE
    include_tables: bool = True
    include_pictures: bool = False
    emit_annotations: bool = True


class ContentStrategy(str, Enum):
    """How the textual content of a replicated document is produced."""

    SYNTHETIC = "synthetic"
    PERTURB = "perturb"
    PRESERVE = "preserve"


class ReplicationOptions(PipelineOptions):
    """Options controlling replication of an existing document."""

    num_variants: int = Field(default=1, ge=1, le=1000)
    content_strategy: ContentStrategy = ContentStrategy.SYNTHETIC
    preserve_layout: bool = True
    preserve_style: bool = True
    preserve_pictures: bool = False
    layout_jitter: float = Field(default=0.0, ge=0.0, le=1.0)
    emit_annotations: bool = True
