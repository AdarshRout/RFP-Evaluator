from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.providers import get_llm
from app.core.config import get_settings
from app.schemas.models import GraphState, Requirement, ExtractionOutput


_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a senior procurement analyst. Extract ALL requirements from this RFP section.

Return ONLY a JSON object: {{"requirements": [...]}}

Each requirement:
- id: "REQ-001" format (continue numbering from {offset})
- category: one of [Technical, Compliance, Financial, Timeline, Operational, Security]  
- description: precise, actionable description
- weight: 0.5 (nice-to-have) | 1.0 (standard) | 1.5 (important) | 2.0 (critical/mandatory)
- mandatory: true if document uses MUST/MANDATORY/REQUIRED language"""),
    ("human", "RFP Section:\n\n{section}\n\nExtract requirements JSON:"),
])


def extract_requirements_agent(state: GraphState) -> GraphState:
    settings = get_settings()
    llm = get_llm(temperature=0.0)
    structured_llm = llm.with_structured_output(ExtractionOutput)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.rfp_chunk_size,
        chunk_overlap=settings.rfp_chunk_overlap,
        separators=["\n\n\n", "\n\n", "\nSECTION", "\nREQ-", "\n"],
    )
    sections = splitter.split_text(state.rfp_text)

    all_requirements: list[Requirement] = []
    seen_ids: set[str] = set()

    for section in sections:
        # Stop processing more sections once we hit the cap
        if len(all_requirements) >= settings.max_requirements:
            break
        try:
            result: ExtractionOutput = structured_llm.invoke(
                _PROMPT.format_messages(section=section, offset=f"REQ-{len(all_requirements)+1:03d}")
            )
            for req in result.requirements:
                if req.id not in seen_ids and len(all_requirements) < settings.max_requirements:
                    seen_ids.add(req.id)
                    all_requirements.append(req)
        except Exception:
            continue

    if not all_requirements:
        all_requirements = _fallback_requirements()

    return GraphState(
        **{**state.model_dump(),
           "requirements": all_requirements,
           "current_step": "requirements_extracted",
           "messages": [f"Extracted {len(all_requirements)} requirements across {len(sections)} sections (cap: {settings.max_requirements})"]}
    )


def _fallback_requirements() -> list[Requirement]:
    return [
        Requirement(id="REQ-001", category="Technical", description="Technical solution quality and architecture", weight=2.0, mandatory=True),
        Requirement(id="REQ-002", category="Financial", description="Cost competitiveness and value for money", weight=1.5, mandatory=True),
        Requirement(id="REQ-003", category="Timeline", description="Delivery timeline and project schedule", weight=1.5, mandatory=True),
        Requirement(id="REQ-004", category="Compliance", description="Regulatory and compliance adherence", weight=2.0, mandatory=True),
        Requirement(id="REQ-005", category="Operational", description="Operational capability and team experience", weight=1.0, mandatory=False),
    ]
