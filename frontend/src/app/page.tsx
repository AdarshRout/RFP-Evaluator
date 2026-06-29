import Link from "next/link";
import { ArrowRight, Cpu, Database, FileSearch, BarChart3, Zap, Lock } from "lucide-react";

const features = [
  { icon: FileSearch, title: "Hierarchical Extraction", desc: "Processes 40+ page RFPs by splitting into sections and extracting requirements chunk by chunk" },
  { icon: Database, title: "RAG Scoring", desc: "Each requirement is scored against semantically retrieved proposal evidence, not LLM memory" },
  { icon: Cpu, title: "LangGraph Orchestration", desc: "4-agent pipeline with typed state, conditional routing, and real-time SSE streaming" },
  { icon: BarChart3, title: "Weighted Analytics", desc: "Category breakdown, radar charts, and weighted scoring that mirrors real procurement logic" },
  { icon: Zap, title: "Structured Outputs", desc: "LangChain structured output with Pydantic schemas — zero fragile JSON parsing" },
  { icon: Lock, title: "Zero Cost Stack", desc: "Groq free tier + HuggingFace embeddings + ChromaDB + Vercel + HF Spaces = $0" },
];

export default function HomePage() {
  return (
    <main className="min-h-screen flex flex-col">
      <nav className="border-b border-surface-border px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 bg-brand rounded-lg flex items-center justify-center text-xs font-bold">AI</div>
          <span className="font-semibold text-white">RFP Evaluator</span>
        </div>
        <Link href="/evaluate" className="btn-primary text-sm flex items-center gap-1.5">
          Start Evaluation <ArrowRight size={14} />
        </Link>
      </nav>

      <section className="flex-1 flex flex-col items-center justify-center px-6 py-24 text-center max-w-4xl mx-auto">
        <div className="inline-flex items-center gap-2 bg-brand/10 border border-brand/20 text-brand text-xs font-semibold px-3 py-1.5 rounded-full mb-6 uppercase tracking-wider">
          LangGraph · LangChain · Groq · ChromaDB
        </div>

        <h1 className="text-5xl font-bold text-white mb-4 leading-tight tracking-tight">
          Agentic RFP<br />
          <span className="text-brand-light">Evaluation System</span>
        </h1>

        <p className="text-muted-light text-lg mb-10 max-w-2xl leading-relaxed">
          A 4-agent AI pipeline that extracts RFP requirements, semantically indexes proposals, scores compliance via RAG, and generates structured evaluation reports — fully automated.
        </p>

        <Link href="/evaluate" className="btn-primary text-base px-6 py-3 flex items-center gap-2">
          Launch Evaluation <ArrowRight size={16} />
        </Link>
      </section>

      <section className="px-6 pb-24 max-w-5xl mx-auto w-full">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {features.map(({ icon: Icon, title, desc }) => (
            <div key={title} className="card p-5 hover:border-brand/30 transition-colors">
              <div className="w-9 h-9 bg-brand/10 rounded-lg flex items-center justify-center mb-3">
                <Icon size={18} className="text-brand-light" />
              </div>
              <h3 className="font-semibold text-white mb-1.5 text-sm">{title}</h3>
              <p className="text-muted text-sm leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
      </section>

      <footer className="border-t border-surface-border px-6 py-4 text-center text-muted text-xs">
        Built for Deloitte T&T EAID — AI Engineer role · Zero cost infrastructure
      </footer>
    </main>
  );
}
