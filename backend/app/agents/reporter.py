from langchain_core.prompts import ChatPromptTemplate
from app.core.providers import get_llm
from app.schemas.models import GraphState, EvaluationReport, RequirementMeta, ReportOutput


_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a senior procurement consultant generating an executive evaluation report.

Return JSON: {{
  "strengths": ["string", ...],
  "gaps": ["string", ...],
  "recommendation": "SHORTLIST | CONDITIONAL | REJECT - one sentence reason",
  "executive_summary": "3-4 sentence assessment"
}}

Recommendation thresholds: SHORTLIST >= 7.5, CONDITIONAL 5.0-7.4, REJECT < 5.0"""),
    ("human", """Vendor: {vendor_name}
Weighted Score: {weighted_score:.1f}/10 | Overall: {overall_score:.1f}/10

Category Scores:
{category_scores}

Top Requirement Results:
{req_summary}

Generate report:"""),
])


def generate_report_agent(state: GraphState) -> GraphState:
    llm = get_llm(temperature=0.2)
    structured_llm = llm.with_structured_output(ReportOutput)

    req_map = {r.id: r for r in state.requirements}

    weighted_total = weight_sum = 0.0
    category_totals: dict[str, list[float]] = {}

    for ps in state.requirement_scores:
        req = req_map.get(ps.requirement_id)
        weight = req.weight if req else 1.0
        weighted_total += ps.score * weight
        weight_sum += weight
        cat = req.category if req else "General"
        category_totals.setdefault(cat, []).append(ps.score)

    overall = sum(ps.score for ps in state.requirement_scores) / len(state.requirement_scores) if state.requirement_scores else 0.0
    weighted = weighted_total / weight_sum if weight_sum > 0 else overall
    category_scores = {cat: round(sum(v) / len(v), 1) for cat, v in category_totals.items()}

    cat_str = "\n".join(f"  {k}: {v}/10" for k, v in category_scores.items())
    req_str = "\n".join(
        f"  [{ps.requirement_id}] {ps.score:.1f}/10 - {ps.justification[:100]}"
        for ps in state.requirement_scores[:12]
    )

    requirements_meta = [
        RequirementMeta(
            id=r.id,
            category=r.category,
            description=r.description,
            weight=r.weight,
            mandatory=r.mandatory,
        )
        for r in state.requirements
    ]

    try:
        result: ReportOutput = structured_llm.invoke(
            _PROMPT.format_messages(
                vendor_name=state.vendor_name,
                weighted_score=weighted,
                overall_score=overall,
                category_scores=cat_str,
                req_summary=req_str,
            )
        )
        report = EvaluationReport(
            vendor_name=state.vendor_name,
            total_score=round(overall, 2),
            weighted_score=round(weighted, 2),
            category_scores=category_scores,
            requirement_scores=state.requirement_scores,
            requirements_meta=requirements_meta,
            strengths=result.strengths,
            gaps=result.gaps,
            recommendation=result.recommendation,
            executive_summary=result.executive_summary,
        )
    except Exception:
        verdict = "SHORTLIST" if weighted >= 7.5 else "CONDITIONAL" if weighted >= 5.0 else "REJECT"
        report = EvaluationReport(
            vendor_name=state.vendor_name,
            total_score=round(overall, 2),
            weighted_score=round(weighted, 2),
            category_scores=category_scores,
            requirement_scores=state.requirement_scores,
            requirements_meta=requirements_meta,
            strengths=["Proposal submitted and evaluated"],
            gaps=["Manual review recommended for detailed assessment"],
            recommendation=f"{verdict} - Automated evaluation completed",
            executive_summary=f"Automated evaluation completed. Weighted score: {weighted:.1f}/10.",
        )

    return GraphState(
        **{**state.model_dump(),
           "report": report,
           "current_step": "complete",
           "messages": [f"Report generated | {report.weighted_score:.1f}/10 | {report.recommendation}"]}
    )
