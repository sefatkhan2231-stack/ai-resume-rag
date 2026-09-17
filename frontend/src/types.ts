// Mirrors backend/app/schemas/resume.py -> ResumeUploadResponse
export interface ResumeUploadResponse {
  resume_id: string;
  candidate_id: string;
  filename: string;
  chunks_indexed: number;
}

// Mirrors backend/app/schemas/job.py -> JobRequirementsResponse
export interface JobRequirements {
  skills: string[];
  tools: string[];
  frameworks: string[];
  databases: string[];
  soft_skills: string[];
}

export interface JobRequirementsResponse {
  requirements: JobRequirements;
  flattened: string[];
}

// Mirrors backend/app/schemas/screening.py -> Evidence / ScreeningResponse
export interface Evidence {
  skill: string;
  text: string;
}

export interface ScreeningResponse {
  candidate: string;
  score: number;
  skills: Record<string, boolean>;
  missing_skills: string[];
  evidence: Evidence[];
  overall_assessment: string;
  final_recommendation: string;
}

// --- Mirrors backend/app/schemas/candidate.py ---

export interface CandidateUploadResult {
  filename: string;
  success: boolean;
  candidate_id: string | null;
  resume_id: string | null;
  chunks_indexed: number | null;
  error: string | null;
}

export interface BatchUploadResponse {
  uploaded: CandidateUploadResult[];
}

export type Recommendation =
  | "Strong Match"
  | "Good Match"
  | "Partial Match"
  | "Weak Match";

export interface RankedCandidate {
  rank: number;
  candidate_id: string;
  resume_id: string;
  name: string;
  email: string | null;
  phone: string | null;
  score: number;
  matched_skills: string[];
  missing_skills: string[];
  recommendation: Recommendation;
}

export interface RankResponse {
  results: RankedCandidate[];
  average_score: number;
  screening_ids: number | null;
}

// --- Mirrors backend/app/schemas/matching.py ---

export interface MatchEvidence {
  skill: string;
  text: string;
}

export interface JobMatchResult {
  rank: number;
  candidate_id: string;
  resume_id: string;
  name: string;
  email: string | null;
  phone: string | null;
  score: number;
  matched_skills: string[];
  missing_skills: string[];
  strengths: string[];
  gaps: string[];
  evidence: MatchEvidence[];
  overall_assessment: string;
  final_recommendation: string;
  recommendation: Recommendation;
}

export interface JobMatchingResponse {
  results: JobMatchResult[];
  average_score: number;
  screening_id: number | null;
}

// --- Mirrors backend/app/schemas/dashboard.py ---

export interface DashboardStats {
  total_resumes: number;
  resumes_today: number;
  resumes_this_week: number;
  resumes_this_month: number;
  resumes_this_year: number;
  total_screenings: number;
  average_match_score: number;
}

export interface ActivityPoint {
  date: string;
  count: number;
}

export interface ScreeningHistoryItem {
  id: number;
  screening_type: "resume_ranking" | "job_matching";
  number_of_resumes: number;
  average_score: number;
  created_at: string;
}
