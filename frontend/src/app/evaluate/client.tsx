"use client";

import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { EvaluationForm } from "@/components/evaluation/EvaluationForm";
import { ResultsDashboard } from "@/components/evaluation/ResultsDashboard";
import { useEvaluationStore } from "@/store/evaluation";

export function EvaluateClient() {
  const { report, status, error } = useEvaluationStore();

  return (
    <div className="min-h-screen flex flex-col">
      <nav className="border-b border-surface-border px-6 py-4 flex items-center gap-4 sticky top-0 bg-surface/95 backdrop-blur z-10">
        <Link href="/" className="text-muted hover:text-white transition-colors p-1">
          <ArrowLeft size={17} />
        </Link>
        <div className="w-px h-4 bg-surface-border" />
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-brand rounded-md flex items-center justify-center text-xs font-bold text-white">
            AI
          </div>
          <span className="font-medium text-white text-sm">RFP Evaluator</span>
        </div>
        <div className="ml-2 flex items-center gap-1 text-xs text-muted">
          <span>LangGraph</span>
          <span className="text-surface-border mx-1">·</span>
          <span>Groq</span>
          <span className="text-surface-border mx-1">·</span>
          <span>ChromaDB</span>
        </div>
        <div className="ml-auto">
          {status === "running" && (
            <div className="flex items-center gap-2 text-xs text-brand">
              <span className="w-1.5 h-1.5 bg-brand rounded-full animate-pulse" />
              Pipeline running
            </div>
          )}
          {status === "complete" && (
            <div className="flex items-center gap-2 text-xs text-success">
              <span className="w-1.5 h-1.5 bg-success rounded-full" />
              Complete
            </div>
          )}
        </div>
      </nav>

      <main className="flex-1 max-w-6xl mx-auto w-full px-6 py-8 space-y-8">
        <div>
          <h1 className="text-2xl font-bold text-white">Evaluate Proposal</h1>
          <p className="text-muted text-sm mt-1">
            Upload RFP and vendor proposal — the 4-agent pipeline extracts requirements, indexes the
            proposal semantically, scores via RAG, and generates a weighted report.
          </p>
        </div>

        <div className="card p-6">
          <EvaluationForm />
        </div>

        {error && (
          <div className="card border-danger/30 bg-danger/5 p-4">
            <p className="text-sm text-danger font-medium">Pipeline error</p>
            <p className="text-xs text-danger/70 mt-1">{error}</p>
          </div>
        )}

        {report && <ResultsDashboard report={report} />}
      </main>

      <footer className="border-t border-surface-border px-6 py-4 text-center text-muted text-xs">
        Built for Deloitte T&T EAID — AI Engineer · Zero cost infrastructure
      </footer>
    </div>
  );
}
