"use client";

import Link from "next/link";
import { Home } from "lucide-react";
import { EvaluationForm } from "@/components/evaluation/EvaluationForm";
import { ResultsDashboard } from "@/components/evaluation/ResultsDashboard";
import { useEvaluationStore } from "@/store/evaluation";

export function EvaluateClient() {
  const { report, status, error } = useEvaluationStore();

  return (
    <div className="min-h-screen flex flex-col">
      <nav className="border-b border-surface-border px-6 py-4 flex items-center gap-4 sticky top-0 bg-surface/95 backdrop-blur z-10">
        <Link
          href="/"
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-brand hover:bg-brand-light text-white text-xs font-semibold shadow-sm transition-all"
        >
          <Home size={14} /> Home
        </Link>
        <div className="w-px h-4 bg-surface-border" />       
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
            Upload RFP and vendor proposal - the 4-agent pipeline extracts requirements, indexes the
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
        Bult by AI by an AI Engineer
      </footer>
    </div>
  );
}
