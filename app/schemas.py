from enum import Enum

from pydantic import BaseModel, Field


class Tone(str, Enum):
    formal = "formal"
    semi_formal = "semi-formal"


class Depth(str, Enum):
    light = "light"
    balanced = "balanced"
    substantial = "substantial"


class RewriteRequest(BaseModel):
    text: str = Field(..., min_length=20, max_length=12000)
    tone: Tone = Tone.formal
    depth: Depth = Depth.balanced
    include_citation_notes: bool = True


class QualityNote(BaseModel):
    label: str
    detail: str


class RewriteResponse(BaseModel):
    original: str
    revised: str
    provider: str
    quality_notes: list[QualityNote]
    academic_integrity_note: str
