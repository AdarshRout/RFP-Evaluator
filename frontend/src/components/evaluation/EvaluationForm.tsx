"use client";

import { useState, useRef } from "react";
import { Upload, FileText, Send, Loader2, RefreshCw, AlertCircle, CheckCircle2, Zap } from "lucide-react";
import { useEvaluationStore } from "@/store/evaluation";

export function EvaluationForm() {
  const [mode, setMode] = useState<"file" | "text">("file");
  const [vendorName, setVendorName] = useState("");
  
  // File inputs
  const [rfpFile, setRfpFile] = useState<File | null>(null);
  const [proposalFile, setProposalFile] = useState<File | null>(null);
  const rfpInputRef = useRef<HTMLInputElement>(null);
  const proposalInputRef = useRef<HTMLInputElement>(null);

  // Text inputs
  const [rfpText, setRfpText] = useState("");
  const [proposalText, setProposalText] = useState("");

  const {
    status,
    currentStep,
    messages,
    progress,
    error,
    startFileEvaluation,
    startTextEvaluation,
    startSampleEvaluation,
    fetchSampleData,
    reset,
  } = useEvaluationStore();

  const isRunning = status === "running";

  const handleLoadSample = async () => {
    const data = await fetchSampleData();
    if (data) {
      setRfpText(data.rfp_text);
      setProposalText(data.proposal_text);
      setVendorName(data.vendor_name);
      setMode("text");
    } else {
      alert("Could not load sample data from server.");
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isRunning) return;

    if (mode === "file") {
      if (!rfpFile || !proposalFile) {
        alert("Please select both RFP and Proposal files.");
        return;
      }
      await startFileEvaluation(rfpFile, proposalFile, vendorName);
    } else {
      if (!rfpText.trim() || !proposalText.trim()) {
        alert("Please enter both RFP text and Proposal text.");
        return;
      }
      await startTextEvaluation(rfpText, proposalText, vendorName);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-surface-border pb-4">
        <div className="flex bg-surface p-1 rounded-lg border border-surface-border">
          <button
            type="button"
            onClick={() => setMode("file")}
            disabled={isRunning}
            className={`flex items-center gap-2 px-4 py-1.5 text-xs font-medium rounded-md transition-all ${
              mode === "file"
                ? "bg-[#92d400] text-black font-bold shadow-sm"
                : "text-muted hover:text-white"
            }`}
          >
            <Upload size={14} /> Upload Documents
          </button>
          <button
            type="button"
            onClick={() => setMode("text")}
            disabled={isRunning}
            className={`flex items-center gap-2 px-4 py-1.5 text-xs font-medium rounded-md transition-all ${
              mode === "text"
                ? "bg-[#92d400] text-black font-bold shadow-sm"
                : "text-muted hover:text-white"
            }`}
          >
            <FileText size={14} /> Paste Text
          </button>
        </div>

        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={handleLoadSample}
            disabled={isRunning}
            className="text-xs bg-brand/10 hover:bg-brand/20 text-brand-light font-semibold px-3 py-1.5 rounded-md border border-brand/20 flex items-center gap-1.5 transition-all"
          >
            <Zap size={13} /> Load Sample Data
          </button>
          <div className="flex items-center gap-2">
            <label className="text-xs text-muted font-medium">Vendor:</label>
            <input
              type="text"
              value={vendorName}
              onChange={(e) => setVendorName(e.target.value)}
              disabled={isRunning}
              placeholder="Vendor Name"
              className="bg-surface border border-surface-border text-xs text-white rounded-md px-3 py-1.5 focus:outline-none focus:border-brand w-44"
            />
          </div>
          {status !== "idle" && (
            <button
              type="button"
              onClick={reset}
              disabled={isRunning}
              className="text-xs text-muted hover:text-white flex items-center gap-1 transition-colors px-2 py-1"
            >
              <RefreshCw size={12} /> Reset
            </button>
          )}
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {mode === "file" ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* RFP File Drop Zone */}
            <div>
              <label className="block text-xs font-semibold text-muted uppercase tracking-wider mb-2">
                RFP Document (Requirements)
              </label>
              <input
                ref={rfpInputRef}
                type="file"
                accept=".txt,.pdf,.docx"
                className="hidden"
                onChange={(e) => setRfpFile(e.target.files?.[0] || null)}
                disabled={isRunning}
              />
              <div
                onClick={() => !isRunning && rfpInputRef.current?.click()}
                className={`border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-all ${
                  rfpFile
                    ? "border-brand bg-brand/5"
                    : "border-surface-border hover:border-brand/50 bg-surface/50"
                }`}
              >
                <div className="w-10 h-10 bg-brand/10 text-brand-light rounded-lg flex items-center justify-center mx-auto mb-3">
                  <Upload size={20} />
                </div>
                {rfpFile ? (
                  <div>
                    <p className="text-sm font-medium text-white truncate max-w-xs mx-auto">
                      {rfpFile.name}
                    </p>
                    <p className="text-xs text-muted mt-1">
                      {(rfpFile.size / 1024).toFixed(1)} KB
                    </p>
                  </div>
                ) : (
                  <div>
                    <p className="text-sm text-white font-medium">Click to upload RFP file</p>
                    <p className="text-xs text-muted mt-1">PDF, DOCX, or TXT format</p>
                  </div>
                )}
              </div>
            </div>

            {/* Proposal File Drop Zone */}
            <div>
              <label className="block text-xs font-semibold text-muted uppercase tracking-wider mb-2">
                Vendor Proposal Document
              </label>
              <input
                ref={proposalInputRef}
                type="file"
                accept=".txt,.pdf,.docx"
                className="hidden"
                onChange={(e) => setProposalFile(e.target.files?.[0] || null)}
                disabled={isRunning}
              />
              <div
                onClick={() => !isRunning && proposalInputRef.current?.click()}
                className={`border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-all ${
                  proposalFile
                    ? "border-brand bg-brand/5"
                    : "border-surface-border hover:border-brand/50 bg-surface/50"
                }`}
              >
                <div className="w-10 h-10 bg-brand/10 text-brand-light rounded-lg flex items-center justify-center mx-auto mb-3">
                  <FileText size={20} />
                </div>
                {proposalFile ? (
                  <div>
                    <p className="text-sm font-medium text-white truncate max-w-xs mx-auto">
                      {proposalFile.name}
                    </p>
                    <p className="text-xs text-muted mt-1">
                      {(proposalFile.size / 1024).toFixed(1)} KB
                    </p>
                  </div>
                ) : (
                  <div>
                    <p className="text-sm text-white font-medium">Click to upload Proposal file</p>
                    <p className="text-xs text-muted mt-1">PDF, DOCX, or TXT format</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-xs font-semibold text-muted uppercase tracking-wider mb-2">
                RFP Content / Requirements
              </label>
              <textarea
                rows={8}
                value={rfpText}
                onChange={(e) => setRfpText(e.target.value)}
                disabled={isRunning}
                placeholder="Paste RFP requirements, specifications, or categories here..."
                className="w-full bg-surface border border-surface-border rounded-xl p-3 text-xs text-white placeholder:text-muted focus:outline-none focus:border-brand font-mono resize-none"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-muted uppercase tracking-wider mb-2">
                Vendor Proposal Content
              </label>
              <textarea
                rows={8}
                value={proposalText}
                onChange={(e) => setProposalText(e.target.value)}
                disabled={isRunning}
                placeholder="Paste vendor proposal responses and solution descriptions here..."
                className="w-full bg-surface border border-surface-border rounded-xl p-3 text-xs text-white placeholder:text-muted focus:outline-none focus:border-brand font-mono resize-none"
              />
            </div>
          </div>
        )}

        <div className="flex flex-col sm:flex-row items-center justify-end gap-3">
          <button
            type="button"
            onClick={startSampleEvaluation}
            disabled={isRunning}
            className="flex items-center gap-2 px-5 py-2.5 text-sm font-semibold rounded-lg bg-[#92d400] hover:bg-[#83be00] text-black transition-all w-full sm:w-auto justify-center shadow-md"
          >
            <Zap size={16} className="text-black" /> Evaluate with Sample Data
          </button>
          <button
            type="submit"
            disabled={isRunning}
            className="flex items-center gap-2 px-6 py-2.5 text-sm font-semibold rounded-lg bg-[#92d400] hover:bg-[#83be00] text-black font-bold shadow-md transition-all w-full sm:w-auto justify-center"
          >
            {isRunning ? (
              <>
                <Loader2 size={16} className="animate-spin text-black" /> Evaluating Proposal...
              </>
            ) : (
              <>
                <Send size={16} className="text-black" /> Run Agentic Evaluation
              </>
            )}
          </button>
        </div>
      </form>

      {/* Progress & SSE Stream Logs */}
      {status !== "idle" && (
        <div className="mt-6 bg-surface p-4 rounded-xl border border-surface-border space-y-3">
          <div className="flex items-center justify-between text-xs font-medium">
            <div className="flex items-center gap-2">
              {isRunning && <Loader2 size={14} className="animate-spin text-brand" />}
              {status === "complete" && <CheckCircle2 size={14} className="text-success" />}
              {status === "error" && <AlertCircle size={14} className="text-danger" />}
              <span className="text-white uppercase tracking-wider font-semibold">
                Pipeline Stage: <span className="text-brand-light">{currentStep || "Initializing"}</span>
              </span>
            </div>
            <span className="text-muted font-mono">{progress}%</span>
          </div>

          <div className="w-full bg-surface-border rounded-full h-2 overflow-hidden">
            <div
              className={`h-full transition-all duration-500 ease-out ${
                status === "error" ? "bg-danger" : status === "complete" ? "bg-success" : "bg-brand"
              }`}
              style={{ width: `${progress}%` }}
            />
          </div>

          {messages.length > 0 && (
            <div className="bg-surface-card rounded-lg p-3 max-h-32 overflow-y-auto font-mono text-[11px] text-muted space-y-1">
              {messages.map((msg, idx) => (
                <div key={idx} className="flex items-start gap-2">
                  <span className="text-brand-light font-bold">›</span>
                  <span className="text-muted-light">{msg}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
