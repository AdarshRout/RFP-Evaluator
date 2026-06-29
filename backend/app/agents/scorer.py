import json
import re
import logging
from langchain_core.prompts import ChatPromptTemplate
from app.core.providers import get_llm
from app.schemas.models import GraphState, ProposalScore, ScoringOutput
from app.agents.indexer import get_store

logger = logging.getLogger(__name__)


_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert procurement evaluator. Score how well the proposal evidence addresses the requirement.

You MUST respond with ONLY a valid JSON object in this exact format:
{{"score": <number 0-10>, "justification": "<2-3 sentence explanation>", "evidence": "<direct quote max 150 chars>"}}

Scoring scale:
9-10: Fully addressed with specific, verifiable details
7-8: Mostly addressed, minor gaps
5-6: Partially addressed or vague claims
3-4: Minimal mention, no substance
0-2: Not addressed or contradicts requirement

Do not include any text outside the JSON object."""),
    ("human", """Requirement: {description}
Category: {category} | Mandatory: {mandatory}

Proposal Evidence:
{evidence}

Respond with JSON only:"""),
])


def _parse_score_from_text(text: str, fallback_evidence: str) -> ScoringOutput:
    """Try to extract score JSON from raw LLM text output when structured output fails."""
    # Try direct JSON parse first
    try:
        data = json.loads(text.strip())
        return ScoringOutput(
            score=float(data["score"]),
            justification=str(data.get("justification", "See evidence.")),
            evidence=str(data.get("evidence", fallback_evidence[:150])),
        )
    except Exception:
        pass

    # Try to extract JSON object from text using regex
    match = re.search(r'\{[^{}]+\}', text, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group())
            return ScoringOutput(
                score=float(data["score"]),
                justification=str(data.get("justification", "Extracted from response.")),
                evidence=str(data.get("evidence", fallback_evidence[:150])),
            )
        except Exception:
            pass

    # Try to extract just a numeric score from the text
    score_match = re.search(r'"score"\s*:\s*([0-9]+(?:\.[0-9]+)?)', text)
    if score_match:
        score = float(score_match.group(1))
        justification_match = re.search(r'"justification"\s*:\s*"([^"]+)"', text)
        evidence_match = re.search(r'"evidence"\s*:\s*"([^"]+)"', text)
        return ScoringOutput(
            score=score,
            justification=justification_match.group(1) if justification_match else "Score parsed from response.",
            evidence=evidence_match.group(1) if evidence_match else fallback_evidence[:150],
        )

    raise ValueError(f"Could not parse score from LLM response: {text[:200]}")


def score_requirements_agent(state: GraphState) -> GraphState:
    llm = get_llm(temperature=0.0)

    session_id = f"{state.vendor_name}_{len(state.rfp_text)}"
    store = get_store(session_id)
    scores: list[ProposalScore] = []

    for req in state.requirements:
        chunks = store.retrieve(req.description)
        evidence = "\n---\n".join(chunks) if chunks else "No relevant content found in the proposal."

        messages = _PROMPT.format_messages(
            description=req.description,
            category=req.category,
            mandatory=req.mandatory,
            evidence=evidence[:2000],
        )

        # Strategy 1: Try with_structured_output (uses tool calling under the hood)
        result: ScoringOutput | None = None
        try:
            structured_llm = llm.with_structured_output(ScoringOutput, method="json_mode")
            result = structured_llm.invoke(messages)
        except Exception as e1:
            logger.warning(f"[{req.id}] structured_output failed: {e1}. Trying raw JSON parse...")

            # Strategy 2: Call LLM directly and parse JSON from text
            try:
                raw_response = llm.invoke(messages)
                raw_text = raw_response.content if hasattr(raw_response, "content") else str(raw_response)
                result = _parse_score_from_text(raw_text, evidence)
            except Exception as e2:
                logger.error(f"[{req.id}] Both scoring strategies failed. e1={e1}, e2={e2}")

        if result is not None:
            scores.append(ProposalScore(
                requirement_id=req.id,
                score=max(0.0, min(10.0, result.score)),
                justification=result.justification,
                evidence=result.evidence,
            ))
        else:
            # True last resort: neutral score with actual evidence
            scores.append(ProposalScore(
                requirement_id=req.id,
                score=5.0,
                justification="Unable to score automatically — manual review recommended.",
                evidence=evidence[:150],
            ))

    return GraphState(
        **{**state.model_dump(),
           "requirement_scores": scores,
           "current_step": "scored",
           "messages": [f"Scored {len(scores)} requirements"]}
    )
