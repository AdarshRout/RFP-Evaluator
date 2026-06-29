"use client";

import { create } from "zustand";
import { EvaluationReport, StreamEvent } from "@/types/evaluation";

interface EvaluationState {
  status: "idle" | "running" | "complete" | "error";
  currentStep: string;
  messages: string[];
  progress: number;
  report: EvaluationReport | null;
  error: string | null;

  startFileEvaluation: (rfpFile: File, proposalFile: File, vendorName: string) => Promise<void>;
  startTextEvaluation: (rfpText: string, proposalText: string, vendorName: string) => Promise<void>;
  startSampleEvaluation: () => Promise<void>;
  fetchSampleData: () => Promise<{ rfp_text: string; proposal_text: string; vendor_name: string } | null>;
  reset: () => void;
}

const rawApiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:7860/api/v1";
const API_BASE_URL = rawApiUrl.endsWith("/api/v1") ? rawApiUrl : `${rawApiUrl.replace(/\/$/, "")}/api/v1`;

export const useEvaluationStore = create<EvaluationState>((set, get) => ({
  status: "idle",
  currentStep: "",
  messages: [],
  progress: 0,
  report: null,
  error: null,

  reset: () =>
    set({
      status: "idle",
      currentStep: "",
      messages: [],
      progress: 0,
      report: null,
      error: null,
    }),

  startFileEvaluation: async (rfpFile, proposalFile, vendorName) => {
    set({
      status: "running",
      currentStep: "init",
      messages: ["Starting evaluation pipeline..."],
      progress: 5,
      report: null,
      error: null,
    });

    const formData = new FormData();
    formData.append("rfp_file", rfpFile);
    formData.append("proposal_file", proposalFile);
    formData.append("vendor_name", vendorName || "Vendor");

    try {
      const response = await fetch(`${API_BASE_URL}/evaluate/stream`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || `Server returned status ${response.status}`);
      }

      await processSSEStream(response, set);
    } catch (err: any) {
      set({
        status: "error",
        error: err.message || "Failed to execute evaluation stream.",
      });
    }
  },

  startTextEvaluation: async (rfpText, proposalText, vendorName) => {
    set({
      status: "running",
      currentStep: "init",
      messages: ["Starting evaluation pipeline..."],
      progress: 5,
      report: null,
      error: null,
    });

    const formData = new FormData();
    formData.append("rfp_text", rfpText);
    formData.append("proposal_text", proposalText);
    formData.append("vendor_name", vendorName || "Vendor");

    try {
      const response = await fetch(`${API_BASE_URL}/evaluate/text`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || `Server returned status ${response.status}`);
      }

      await processSSEStream(response, set);
    } catch (err: any) {
      set({
        status: "error",
        error: err.message || "Failed to execute evaluation stream.",
      });
    }
  },

  startSampleEvaluation: async () => {
    set({
      status: "running",
      currentStep: "init",
      messages: ["Starting evaluation with sample Cloud ERP dataset..."],
      progress: 5,
      report: null,
      error: null,
    });

    try {
      const response = await fetch(`${API_BASE_URL}/evaluate/sample`, {
        method: "POST",
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || `Server returned status ${response.status}`);
      }

      await processSSEStream(response, set);
    } catch (err: any) {
      set({
        status: "error",
        error: err.message || "Failed to execute sample evaluation stream.",
      });
    }
  },

  fetchSampleData: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/evaluate/sample-data`);
      if (!response.ok) return null;
      return await response.json();
    } catch (e) {
      return null;
    }
  },
}));

async function processSSEStream(response: Response, set: any) {
  const reader = response.body?.getReader();
  if (!reader) throw new Error("ReadableStream not supported in browser.");

  const decoder = new TextDecoder("utf-8");
  let buffer = "";

  const stepProgressMap: Record<string, number> = {
    init: 5,
    extract_requirements: 30,
    index_proposal: 55,
    score_requirements: 85,
    generate_report: 98,
    complete: 100,
  };

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n\n");
    buffer = lines.pop() || "";

    for (const line of lines) {
      const trimmed = line.trim();
      if (trimmed.startsWith("data:")) {
        const jsonStr = trimmed.replace(/^data:\s*/, "");
        try {
          const event = JSON.parse(jsonStr);

          if (event.event === "status") {
            // Pre-step announcement
            const step = event.step || "processing";
            const progress = stepProgressMap[step] || 50;
            set((state: EvaluationState) => ({
              currentStep: step,
              progress,
              messages: event.message ? [...state.messages, event.message] : state.messages,
            }));
          } else if (event.event === "step_complete") {
            // Post-step completion update
            const step = event.step || "processing";
            const progress = stepProgressMap[step] || 50;
            set((state: EvaluationState) => ({
              currentStep: step,
              progress,
              messages: event.message ? [...state.messages, event.message] : state.messages,
            }));
          } else if (event.event === "report") {
            // Final report delivered
            set({
              report: event.data,
              status: "complete",
              progress: 100,
              currentStep: "complete",
            });
          } else if (event.event === "complete") {
            // Pipeline done signal without report (fallback)
            set((state: EvaluationState) => ({
              status: state.report ? "complete" : state.status,
              progress: 100,
              currentStep: "complete",
              messages: event.message ? [...state.messages, event.message] : state.messages,
            }));
          } else if (event.event === "error") {
            set({
              status: "error",
              error: event.error || "An error occurred during evaluation.",
            });
          }
        } catch (e) {
          console.error("Error parsing SSE event:", e, jsonStr);
        }
      }
    }
  }
}
