import asyncio
from functools import lru_cache, partial
from typing import AsyncGenerator
from langgraph.graph import StateGraph, START, END
from app.schemas.models import GraphState
from app.agents.extractor import extract_requirements_agent
from app.agents.indexer import index_proposal_agent
from app.agents.scorer import score_requirements_agent
from app.agents.reporter import generate_report_agent


def _build_graph():
    g = StateGraph(GraphState)
    g.add_node("extract_requirements", extract_requirements_agent)
    g.add_node("index_proposal", index_proposal_agent)
    g.add_node("score_requirements", score_requirements_agent)
    g.add_node("generate_report", generate_report_agent)
    g.add_edge(START, "extract_requirements")
    g.add_edge("extract_requirements", "index_proposal")
    g.add_edge("index_proposal", "score_requirements")
    g.add_edge("score_requirements", "generate_report")
    g.add_edge("generate_report", END)
    return g.compile()


@lru_cache(maxsize=1)
def get_graph():
    return _build_graph()


async def _run_agent_in_thread(agent_fn, state: GraphState) -> GraphState:
    """Run a synchronous agent function in a thread pool to avoid blocking the asyncio event loop."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, agent_fn, state)


async def stream_evaluation(rfp_text: str, proposal_text: str, vendor_name: str) -> AsyncGenerator[dict, None]:
    initial = GraphState(rfp_text=rfp_text, proposal_text=proposal_text, vendor_name=vendor_name)

    step_labels = {
        "extract_requirements": "Extracting RFP requirements",
        "index_proposal": "Indexing proposal into vector store",
        "score_requirements": "Scoring requirements via RAG",
        "generate_report": "Generating evaluation report",
    }

    steps = [
        ("extract_requirements", extract_requirements_agent),
        ("index_proposal", index_proposal_agent),
        ("score_requirements", score_requirements_agent),
        ("generate_report", generate_report_agent),
    ]

    state = initial
    for node_name, agent_fn in steps:
        yield {
            "event": "status",
            "step": node_name,
            "label": step_labels[node_name],
            "message": f"Starting: {step_labels[node_name]}...",
            "current_step": node_name,
        }

        # Run synchronous LLM-heavy agent in a thread pool - never blocks the event loop
        state = await _run_agent_in_thread(agent_fn, state)

        yield {
            "event": "step_complete" if node_name != "generate_report" else "report",
            "step": node_name,
            "label": step_labels[node_name],
            "message": state.messages[-1] if state.messages else "",
            "current_step": state.current_step,
            "data": state.report.model_dump() if state.report else None,
        }

    yield {"event": "complete", "message": "Evaluation complete"}

