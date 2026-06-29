"use client";

import { useState } from "react";
import { EvaluationReport } from "@/types/evaluation";
import { Award, CheckCircle, AlertTriangle, FileSpreadsheet, FileText, Download, Check, X } from "lucide-react";

interface ResultsDashboardProps {
  report: EvaluationReport;
}

const rawApiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:7860/api/v1";
const API_BASE_URL = rawApiUrl.endsWith("/api/v1") ? rawApiUrl : `${rawApiUrl.replace(/\/$/, "")}/api/v1`;

export function ResultsDashboard({ report }: ResultsDashboardProps) {
  const [activeTab, setActiveTab] = useState<"summary" | "analysis" | "requirements">("summary");
  const [downloadingFormat, setDownloadingFormat] = useState<string | null>(null);

  const handleExport = async (format: "pdf" | "docx" | "xlsx") => {
    setDownloadingFormat(format);
    try {
      const response = await fetch(`${API_BASE_URL}/evaluate/export/${format}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(report),
      });

      if (!response.ok) throw new Error(`Export failed with status ${response.status}`);

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `rfp_report_${report.vendor_name.replace(/\s+/g, "_")}.${format}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err: any) {
      alert(`Error exporting report: ${err.message}`);
    } finally {
      setDownloadingFormat(null);
    }
  };

  // scores from backend are 0-10
  const getScoreColor = (score: number) => {
    if (score >= 8.0) return "text-success bg-success/10 border-success/20";
    if (score >= 6.0) return "text-warning bg-warning/10 border-warning/20";
    return "text-danger bg-danger/10 border-danger/20";
  };

  const fmtScore = (score: number) => `${(score * 10).toFixed(1)}%`;

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Top Banner Summary Card */}
      <div className="card p-6 bg-gradient-to-r from-surface-card to-surface border-brand/30">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-brand/10 border border-brand/20 text-brand-light text-xs font-semibold uppercase tracking-wider">
              <Award size={14} /> Official Evaluation Report
            </div>
            <h2 className="text-3xl font-bold text-white tracking-tight">{report.vendor_name}</h2>
            <p className="text-xs text-muted">
              Recommendation:{" "}
              <span className="font-semibold text-white px-2 py-0.5 rounded bg-surface-border">
                {report.recommendation}
              </span>
            </p>
          </div>

          <div className="flex items-center gap-6 bg-surface p-4 rounded-xl border border-surface-border">
            <div className="text-center px-4 border-r border-surface-border">
              <div className="text-2xl font-bold font-mono text-white">
                {fmtScore(report.total_score)}
              </div>
              <div className="text-[10px] uppercase text-muted font-medium mt-0.5">Raw Compliance</div>
            </div>
            <div className="text-center px-4">
              <div className="text-3xl font-extrabold font-mono text-brand-light">
                {fmtScore(report.weighted_score)}
              </div>
              <div className="text-[10px] uppercase text-brand font-bold mt-0.5">Weighted Score</div>
            </div>
          </div>
        </div>

        {/* Category breakdown progress mini-bars */}
        <div className="mt-6 pt-6 border-t border-surface-border grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {Object.entries(report.category_scores).map(([category, score]) => (
            <div key={category} className="bg-surface-card p-3 rounded-lg border border-surface-border">
              <div className="flex justify-between text-xs font-medium mb-1.5">
                <span className="text-muted-light truncate">{category}</span>
                <span className="font-mono font-semibold text-white">{fmtScore(score)}</span>
              </div>
              <div className="w-full bg-surface-border rounded-full h-1.5 overflow-hidden">
                <div
                  className="bg-brand-light h-full rounded-full transition-all duration-500"
                  style={{ width: `${Math.min(100, Math.max(0, score * 10))}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Export & Navigation Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-surface-border pb-3">
        <div className="flex gap-2 border-b sm:border-b-0 border-surface-border pb-2 sm:pb-0">
          <button
            onClick={() => setActiveTab("summary")}
            className={`px-4 py-2 text-xs font-semibold rounded-lg transition-all ${
              activeTab === "summary"
                ? "bg-brand text-white shadow-sm"
                : "text-muted hover:text-white"
            }`}
          >
            Executive Summary
          </button>
          <button
            onClick={() => setActiveTab("analysis")}
            className={`px-4 py-2 text-xs font-semibold rounded-lg transition-all ${
              activeTab === "analysis"
                ? "bg-brand text-white shadow-sm"
                : "text-muted hover:text-white"
            }`}
          >
            Strengths & Gaps ({report.strengths.length + report.gaps.length})
          </button>
          <button
            onClick={() => setActiveTab("requirements")}
            className={`px-4 py-2 text-xs font-semibold rounded-lg transition-all ${
              activeTab === "requirements"
                ? "bg-brand text-white shadow-sm"
                : "text-muted hover:text-white"
            }`}
          >
            Detailed Requirements ({report.requirement_scores.length})
          </button>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => handleExport("pdf")}
            disabled={downloadingFormat !== null}
            className="btn-ghost text-xs flex items-center gap-1.5 py-1.5 px-3"
          >
            <FileText size={14} className="text-danger" /> PDF
          </button>
          <button
            onClick={() => handleExport("docx")}
            disabled={downloadingFormat !== null}
            className="btn-ghost text-xs flex items-center gap-1.5 py-1.5 px-3"
          >
            <Download size={14} className="text-brand-light" /> DOCX
          </button>
          <button
            onClick={() => handleExport("xlsx")}
            disabled={downloadingFormat !== null}
            className="btn-ghost text-xs flex items-center gap-1.5 py-1.5 px-3"
          >
            <FileSpreadsheet size={14} className="text-success" /> Excel
          </button>
        </div>
      </div>

      {/* Tab Contents */}
      {activeTab === "summary" && (
        <div className="space-y-6 animate-fade-in">
          <div className="card p-6">
            <h3 className="text-sm font-bold uppercase tracking-wider text-white mb-3">Executive Summary</h3>
            <p className="text-sm text-muted-light leading-relaxed whitespace-pre-line">
              {report.executive_summary}
            </p>
          </div>

          <div className="card p-6 border-brand/20 bg-brand/5">
            <h3 className="text-sm font-bold uppercase tracking-wider text-brand-light mb-2">Final Recommendation</h3>
            <p className="text-sm text-white font-medium">{report.recommendation}</p>
          </div>
        </div>
      )}

      {activeTab === "analysis" && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 animate-fade-in">
          {/* Strengths */}
          <div className="card p-6 border-success/30 bg-success/5 space-y-4">
            <div className="flex items-center gap-2 text-success font-bold text-sm uppercase tracking-wider">
              <CheckCircle size={18} /> Identified Strengths ({report.strengths.length})
            </div>
            <ul className="space-y-2.5">
              {report.strengths.map((strength, idx) => (
                <li key={idx} className="flex items-start gap-2.5 text-xs text-muted-light leading-relaxed">
                  <span className="w-1.5 h-1.5 rounded-full bg-success mt-1.5 shrink-0" />
                  <span>{strength}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Gaps */}
          <div className="card p-6 border-danger/30 bg-danger/5 space-y-4">
            <div className="flex items-center gap-2 text-danger font-bold text-sm uppercase tracking-wider">
              <AlertTriangle size={18} /> Key Gaps & Concerns ({report.gaps.length})
            </div>
            <ul className="space-y-2.5">
              {report.gaps.map((gap, idx) => (
                <li key={idx} className="flex items-start gap-2.5 text-xs text-muted-light leading-relaxed">
                  <span className="w-1.5 h-1.5 rounded-full bg-danger mt-1.5 shrink-0" />
                  <span>{gap}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {activeTab === "requirements" && (
        <div className="card overflow-hidden animate-fade-in">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-surface-border bg-surface-card/80 text-[11px] font-semibold text-muted uppercase tracking-wider">
                  <th className="py-3 px-4">Req ID</th>
                  <th className="py-3 px-4">Score</th>
                  <th className="py-3 px-4">Retrieved Proposal Evidence</th>
                  <th className="py-3 px-4">AI Justification</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-surface-border text-xs">
                {report.requirement_scores.map((item) => {
                  const meta = report.requirements_meta?.find((m) => m.id === item.requirement_id);
                  return (
                    <tr key={item.requirement_id} className="hover:bg-surface-hover/50 transition-colors">
                      <td className="py-3 px-4 font-mono font-bold text-white align-top whitespace-nowrap">
                        {item.requirement_id}
                        {meta && (
                          <div className="text-[10px] text-muted font-normal mt-0.5 max-w-[150px] truncate">
                            {meta.category}
                          </div>
                        )}
                      </td>
                      <td className="py-3 px-4 align-top whitespace-nowrap">
                        <span className={`inline-block font-mono px-2 py-0.5 rounded border font-bold text-xs ${getScoreColor(item.score)}`}>
                          {item.score.toFixed(1)}/10
                        </span>
                      </td>
                      <td className="py-3 px-4 align-top text-muted-light font-mono text-[11px] max-w-md leading-relaxed bg-surface/30">
                        {item.evidence ? (
                          <p className="line-clamp-3 hover:line-clamp-none transition-all cursor-pointer">
                            "{item.evidence}"
                          </p>
                        ) : (
                          <span className="text-muted italic">No specific evidence retrieved</span>
                        )}
                      </td>
                      <td className="py-3 px-4 align-top text-muted-light leading-relaxed max-w-sm">
                        {item.justification}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
