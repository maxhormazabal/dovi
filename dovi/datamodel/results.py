from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from dovi.datamodel.base_models import ErrorItem, TaskStatus
from dovi.datamodel.document import DoviDocument


class RenderedArtifact(BaseModel):
    path: Path
    media_type: str


class GenerationResult(BaseModel):
    status: TaskStatus = TaskStatus.PENDING
    document: DoviDocument | None = None
    artifacts: list[RenderedArtifact] = Field(default_factory=list)
    errors: list[ErrorItem] = Field(default_factory=list)
    timings: dict[str, float] = Field(default_factory=dict)


class ReplicationResult(BaseModel):
    status: TaskStatus = TaskStatus.PENDING
    source: Path
    source_document: DoviDocument | None = None
    documents: list[DoviDocument] = Field(default_factory=list)
    artifacts: list[RenderedArtifact] = Field(default_factory=list)
    errors: list[ErrorItem] = Field(default_factory=list)
    timings: dict[str, float] = Field(default_factory=dict)
