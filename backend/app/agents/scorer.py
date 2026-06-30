import json
import re
import logging
import time
from concurrent.futures import ThreadPoolExecutor
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


def _score_single(req, store, llm):
    t0 = time.perf_counter()
    print(f"  [SCORER] [{req.id}] ▶ Starting | category={req.category} | mandatory={req.mandatory}")

    # --- Retrieval ---
    t_ret = time.perf_counter()
    chunks = store.retrieve(req.description)
    print(f"  [SCORER] [{req.id}] 🔍 Retrieval done in {time.perf_counter() - t_ret:.2f}s | chunks={len(chunks) if chunks else 0}")

    evidence = "\n---\n".join(chunks) if chunks else "No relevant content found in the proposal."
    if not chunks:
        print(f"  [SCORER] [{req.id}] ⚠️  WARNING: No chunks retrieved — evidence will be empty. Score may fall back to default.")

    messages = _PROMPT.format_messages(
        description=req.description,
        category=req.category,
        mandatory=req.mandatory,
        evidence=evidence[:800],
    )

    # --- Strategy 1: structured_output ---
    t_llm = time.perf_counter()
    print(f"  [SCORER] [{req.id}] 🤖 Calling LLM (structured_output)...")
    try:
        structured_llm = llm.with_structured_output(ScoringOutput, method="json_mode")
        result = structured_llm.invoke(messages)
        elapsed = time.perf_counter() - t_llm
        print(f"  [SCORER] [{req.id}] ✅ structured_output succeeded in {elapsed:.2f}s | score={result.score:.1f}")
        print(f"  [SCORER] [{req.id}] ⏱  Total time: {time.perf_counter() - t0:.2f}s")
        return req, result, evidence
    except Exception as e1:
        elapsed = time.perf_counter() - t_llm
        print(f"  [SCORER] [{req.id}] ❌ structured_output FAILED after {elapsed:.2f}s | error={e1}")
        logger.warning(f"[{req.id}] structured_output failed: {e1}. Trying raw JSON parse...")

    # --- Strategy 2: raw LLM + text parse ---
    t_llm2 = time.perf_counter()
    print(f"  [SCORER] [{req.id}] 🔄 Falling back to raw LLM invoke...")
    try:
        raw = llm.invoke(messages)
        text = raw.content if hasattr(raw, "content") else str(raw)
        result = _parse_score_from_text(text, evidence)
        elapsed = time.perf_counter() - t_llm2
        print(f"  [SCORER] [{req.id}] ✅ raw LLM parse succeeded in {elapsed:.2f}s | score={result.score:.1f}")
        print(f"  [SCORER] [{req.id}] ⏱  Total time: {time.perf_counter() - t0:.2f}s")
        return req, result, evidence
    except Exception as e2:
        elapsed = time.perf_counter() - t_llm2
        print(f"  [SCORER] [{req.id}] ❌ raw LLM parse FAILED after {elapsed:.2f}s | error={e2}")
        logger.error(f"[{req.id}] Both scoring strategies failed. e1={e1}, e2={e2}")
        print(f"  [SCORER] [{req.id}] 🚨 FALLBACK: returning None — will use neutral score=5.0")
        print(f"  [SCORER] [{req.id}] ⏱  Total time: {time.perf_counter() - t0:.2f}s")
        return req, None, evidence


def score_requirements_agent(state: GraphState) -> GraphState:
    total_reqs = len(state.requirements)
    print(f"\n[SCORER] ========== score_requirements_agent START ==========")
    print(f"[SCORER] Vendor: {state.vendor_name} | Requirements to score: {total_reqs}")

    t_start = time.perf_counter()
    llm = get_llm(temperature=0.0)
    session_id = f"{state.vendor_name}_{len(state.rfp_text)}"
    store = get_store(session_id)
    scores: list[ProposalScore] = []

    print(f"[SCORER] Dispatching {total_reqs} requirements to ThreadPoolExecutor (max_workers=5)...")

    with ThreadPoolExecutor(max_workers=5) as executor:  # Groq rate limit safe
        futures = [
            executor.submit(_score_single, req, store, llm)
            for req in state.requirements
        ]
        completed = 0
        for fut in futures:
            req, result, evidence = fut.result()
            completed += 1
            if result is not None:
                clamped_score = max(0.0, min(10.0, result.score))
                scores.append(ProposalScore(
                    requirement_id=req.id,
                    score=clamped_score,
                    justification=result.justification,
                    evidence=result.evidence,
                ))
                print(f"[SCORER] ({completed}/{total_reqs}) ✅ [{req.id}] scored={clamped_score:.1f}")
            else:
                # True last resort: neutral score with actual evidence
                scores.append(ProposalScore(
                    requirement_id=req.id,
                    score=5.0,
                    justification="Unable to score automatically - manual review recommended.",
                    evidence=evidence[:800],
                ))
                print(f"[SCORER] ({completed}/{total_reqs}) 🚨 [{req.id}] FALLBACK score=5.0 (both LLM strategies failed)")

    elapsed_total = time.perf_counter() - t_start
    fallback_count = sum(1 for s in scores if s.score == 5.0 and "manual review" in s.justification)
    print(f"[SCORER] ========== score_requirements_agent DONE ==========")
    print(f"[SCORER] Total time: {elapsed_total:.2f}s | Scored: {len(scores)} | Fallbacks: {fallback_count}/{total_reqs}")
    if fallback_count > 0:
        fallback_ids = [s.requirement_id for s in scores if s.score == 5.0 and "manual review" in s.justification]
        print(f"[SCORER] ⚠️  Fallback requirement IDs: {fallback_ids}")
    print()

    return GraphState(
        **{**state.model_dump(),
           "requirement_scores": scores,
           "current_step": "scored",
           "messages": [f"Scored {len(scores)} requirements"]}
    )
