from app.schemas.models import GraphState
from app.services.vector_store import VectorStoreService

_store_registry: dict[str, VectorStoreService] = {}


def get_store(session_id: str) -> VectorStoreService:
    if session_id not in _store_registry:
        _store_registry[session_id] = VectorStoreService()
    return _store_registry[session_id]


def index_proposal_agent(state: GraphState) -> GraphState:
    session_id = f"{state.vendor_name}_{len(state.rfp_text)}"
    store = get_store(session_id)
    chunks = store.index(state.proposal_text, state.vendor_name)

    return GraphState(
        **{**state.model_dump(),
           "proposal_chunks": chunks,
           "current_step": "proposal_indexed",
           "messages": [f"Indexed {len(chunks)} proposal chunks into vector store"]}
    )
