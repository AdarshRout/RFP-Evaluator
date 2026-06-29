from functools import lru_cache
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


async def stream_evaluation(rfp_text: str, proposal_text: str, vendor_name: str) -> AsyncGenerator[dict, None]:
    graph = get_graph()
    initial = GraphState(rfp_text=rfp_text, proposal_text=proposal_text, vendor_name=vendor_name)

    step_labels = {
        "extract_requirements": "Extracting RFP requirements",
        "index_proposal": "Indexing proposal into vector store",
        "score_requirements": "Scoring requirements via RAG",
        "generate_report": "Generating evaluation report",
    }

    async for event in graph.astream(initial.model_dump(), stream_mode="updates"):
        for node_name, node_state in event.items():
            if node_name == "__end__":
                continue
            state = GraphState(**node_state) if isinstance(node_state, dict) else node_state
            yield {
                "event": "step_complete",
                "step": node_name,
                "label": step_labels.get(node_name, node_name),
                "message": state.messages[-1] if state.messages else "",
                "current_step": state.current_step,
                "report": state.report.model_dump() if state.report else None,
            }

    yield {"event": "done"}
