from langchain_core.prompts import ChatPromptTemplate
from app.core.providers import get_llm
from app.schemas.models import GraphState, ProposalScore, ScoringOutput
from app.agents.indexer import get_store


_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert procurement evaluator. Score how well the proposal evidence addresses the requirement.

Return JSON: {{"score": float, "justification": "2-3 sentences", "evidence": "direct quote max 150 chars"}}

Scoring:
9-10: Fully addressed with specific, verifiable details
7-8: Mostly addressed, minor gaps
5-6: Partially addressed or vague claims
3-4: Minimal mention, no substance  
0-2: Not addressed or contradicts requirement"""),
    ("human", """Requirement: {description}
Category: {category} | Mandatory: {mandatory}

Proposal Evidence:
{evidence}

Score:"""),
])


def score_requirements_agent(state: GraphState) -> GraphState:
    llm = get_llm(temperature=0.0)
    structured_llm = llm.with_structured_output(ScoringOutput)

    session_id = f"{state.vendor_name}_{len(state.rfp_text)}"
    store = get_store(session_id)
    scores: list[ProposalScore] = []

    for req in state.requirements:
        chunks = store.retrieve(req.description)
        evidence = "\n---\n".join(chunks) if chunks else "No relevant content found."

        try:
            result: ScoringOutput = structured_llm.invoke(
                _PROMPT.format_messages(
                    description=req.description,
                    category=req.category,
                    mandatory=req.mandatory,
                    evidence=evidence[:2000],
                )
            )
            scores.append(ProposalScore(
                requirement_id=req.id,
                score=max(0.0, min(10.0, result.score)),
                justification=result.justification,
                evidence=result.evidence,
            ))
        except Exception:
            scores.append(ProposalScore(
                requirement_id=req.id,
                score=5.0,
                justification="Score defaulted due to processing error.",
                evidence=evidence[:150],
            ))

    return GraphState(
        **{**state.model_dump(),
           "requirement_scores": scores,
           "current_step": "scored",
           "messages": [f"Scored {len(scores)} requirements"]}
    )
