from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Annotated
import operator


class Requirement(BaseModel):
    id: str
    category: str
    description: str
    weight: float = 1.0
    mandatory: bool = False


class ProposalScore(BaseModel):
    requirement_id: str
    score: float
    justification: str
    evidence: str


class RequirementMeta(BaseModel):
    id: str
    category: str
    description: str
    weight: float
    mandatory: bool


class EvaluationReport(BaseModel):
    vendor_name: str
    total_score: float
    weighted_score: float
    category_scores: dict[str, float]
    requirement_scores: list[ProposalScore]
    requirements_meta: list[RequirementMeta] = Field(default_factory=list)
    strengths: list[str]
    gaps: list[str]
    recommendation: str
    executive_summary: str


class GraphState(BaseModel):
    rfp_text: str = ""
    proposal_text: str = ""
    vendor_name: str = "Vendor"
    requirements: list[Requirement] = Field(default_factory=list)
    proposal_chunks: list[str] = Field(default_factory=list)
    requirement_scores: list[ProposalScore] = Field(default_factory=list)
    report: Optional[EvaluationReport] = None
    error: Optional[str] = None
    current_step: str = "init"
    messages: Annotated[list[str], operator.add] = Field(default_factory=list)


class EvaluationRequest(BaseModel):
    rfp_text: str
    proposal_text: str
    vendor_name: str = "Vendor"


class StreamEvent(BaseModel):
    event: str
    step: Optional[str] = None
    message: Optional[str] = None
    data: Optional[dict] = None
    error: Optional[str] = None


class ExtractionOutput(BaseModel):
    requirements: list[Requirement]


class ScoringOutput(BaseModel):
    score: float
    justification: str
    evidence: str


class ReportOutput(BaseModel):
    strengths: list[str]
    gaps: list[str]
    recommendation: str
    executive_summary: str
