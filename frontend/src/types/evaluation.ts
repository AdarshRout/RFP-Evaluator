export interface Requirement {
  id: string;
  category: string;
  description: string;
  weight: number;
  mandatory: boolean;
}

export interface ProposalScore {
  requirement_id: string;
  score: number;
  justification: string;
  evidence: string;
}

export interface RequirementMeta {
  id: string;
  category: string;
  description: string;
  weight: number;
  mandatory: boolean;
}

export interface EvaluationReport {
  vendor_name: string;
  total_score: number;
  weighted_score: number;
  category_scores: Record<string, number>;
  requirement_scores: ProposalScore[];
  requirements_meta?: RequirementMeta[];
  strengths: string[];
  gaps: string[];
  recommendation: string;
  executive_summary: string;
}

export interface StreamEvent {
  event: 'status' | 'report' | 'error' | 'complete';
  step?: string;
  message?: string;
  data?: EvaluationReport | any;
  error?: string;
}
