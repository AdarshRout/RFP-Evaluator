# RFP Evaluator - Enterprise Agentic AI Platform

**Stack:** Next.js 15 · FastAPI · LangGraph · LangChain · Groq (Llama 3.3-70B) · ChromaDB · sentence-transformers  
**Deployment:** Vercel (frontend) + Hugging Face Spaces (backend) · **$0 total cost**

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Next.js 15 (Vercel)                                        │
│  ┌──────────────┐  SSE stream  ┌──────────────────────────┐ │
│  │  EvaluateUI  │◄────────────►│  FastAPI (HF Spaces)     │ │
│  │  Zustand     │              │  ┌──────────────────────┐ │ │
│  │  Recharts    │  POST /file  │  │  LangGraph Pipeline  │ │ │
│  └──────────────┘              │  │  ① Extractor Agent   │ │ │
│                                │  │  ② Indexer Agent     │ │ │
│                                │  │  ③ Scorer Agent      │ │ │
│                                │  │  ④ Reporter Agent    │ │ │
│                                │  └──────────────────────┘ │ │
│                                │  ChromaDB · HF Embeddings  │ │
│                                └──────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## Local Development

### Backend

```bash
cd backend
cp .env.example .env
# Edit .env - set GROQ_API_KEY=gsk_your_key_here

pip install -r requirements.txt
uvicorn app.main:app --reload --port 7860
# API docs: http://localhost:7860/docs
```

### Frontend

```bash
cd frontend
cp .env.example .env.local
# Edit .env.local - set NEXT_PUBLIC_API_URL=http://localhost:7860

npm install
npm run dev
# App: http://localhost:3000
```

---

## Deploy Backend → Hugging Face Spaces (Free)

1. Go to [huggingface.co](https://huggingface.co) → **New Space**
2. Settings:
   - SDK: **Docker**
   - Space name: `rfp-evaluator-api`
   - Visibility: Public
3. Upload the entire `backend/` folder contents (not the folder itself)
4. In Space **Settings → Repository Secrets**, add:
   ```
   GROQ_API_KEY = gsk_your_key_here
   ```
5. Space builds automatically (~3–5 min). Note your Space URL:
   `https://YOUR_USERNAME-rfp-evaluator-api.hf.space`

---

## Deploy Frontend → Vercel (Free)

**Option A - Vercel CLI:**
```bash
cd frontend
npx vercel
# Follow prompts → set environment variable when asked:
# NEXT_PUBLIC_API_URL = https://YOUR_USERNAME-rfp-evaluator-api.hf.space
```

**Option B - GitHub import:**
1. Push `frontend/` to a GitHub repo
2. Go to [vercel.com](https://vercel.com) → **Add New Project** → import repo
3. Root directory: `frontend`
4. Environment variables:
   ```
   NEXT_PUBLIC_API_URL = https://YOUR_USERNAME-rfp-evaluator-api.hf.space
   ```
5. Deploy

---

## Project Structure

```
rfp-platform/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── extractor.py      # Agent 1: hierarchical RFP extraction
│   │   │   ├── indexer.py        # Agent 2: ChromaDB semantic indexing
│   │   │   ├── scorer.py         # Agent 3: RAG-based requirement scoring
│   │   │   └── reporter.py       # Agent 4: weighted report generation
│   │   ├── api/v1/routes/
│   │   │   ├── evaluation.py     # SSE stream + export endpoints
│   │   │   └── health.py
│   │   ├── core/
│   │   │   ├── config.py         # Pydantic settings (reads .env)
│   │   │   ├── pipeline.py       # LangGraph graph + astream()
│   │   │   └── providers.py      # LLM + embeddings (cached)
│   │   ├── schemas/models.py     # All Pydantic domain models
│   │   ├── services/
│   │   │   ├── export_service.py # PDF + DOCX + XLSX export
│   │   │   └── vector_store.py   # Per-session ChromaDB service
│   │   └── utils/document_parser.py
│   ├── Dockerfile
│   └── requirements.txt
│
└── frontend/
    └── src/
        ├── app/
        │   ├── page.tsx              # Landing page
        │   └── evaluate/
        │       ├── page.tsx          # Server component wrapper
        │       └── client.tsx        # Client root
        ├── components/
        │   ├── evaluation/
        │   │   ├── EvaluationForm.tsx     # Upload + trigger + pipeline progress
        │   │   ├── ResultsDashboard.tsx   # Full report view
        │   │   ├── PipelineProgress.tsx   # Live step tracker
        │   │   ├── ScoreGauge.tsx         # SVG circular gauge
        │   │   ├── CategoryRadar.tsx      # Recharts radar
        │   │   ├── CategoryBar.tsx        # Recharts horizontal bar
        │   │   ├── RequirementsTable.tsx  # Sortable + expandable table
        │   │   └── ExportButtons.tsx      # PDF / DOCX / XLSX
        │   └── ui/FileDropzone.tsx
        ├── lib/
        │   ├── api/client.ts         # SSE stream + export fetch
        │   ├── hooks/useEvaluation.ts
        │   └── utils/index.ts
        ├── store/evaluation.ts       # Zustand store
        └── types/index.ts
```

---

## Key Technical Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| LLM | Groq Llama 3.3-70B | Free, fastest inference (LPU), no card required |
| Structured output | `with_structured_output()` | Zero fragile JSON parsing - Pydantic schema enforced |
| RFP extraction | Hierarchical chunking | Handles 40+ page docs; per-section extraction |
| Vector store | ChromaDB ephemeral | Zero config, session-isolated, no server needed |
| Streaming | LangGraph `astream()` + SSE | Real-time step progress to frontend |
| Embeddings | sentence-transformers local | No API cost; data privacy (never leaves server) |
| Frontend state | Zustand | Lightweight, no boilerplate, SSE-friendly |
| Hosting | HF Spaces (Docker) + Vercel | Both free tiers, production-grade |
