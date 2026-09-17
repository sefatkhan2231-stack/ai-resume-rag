import type { JobRequirementsResponse, ScreeningResponse } from "../types";
import request from "./client";

export function analyzeJobDescription(
  jobDescription: string,
): Promise<JobRequirementsResponse> {
  return request<JobRequirementsResponse>("/jobs/analyze", {
    method: "POST",
    body: { job_description: jobDescription },
  });
}

export function screenCandidate(
  jobDescription: string,
  candidateId: string,
  candidateName = "Candidate",
): Promise<ScreeningResponse> {
  return request<ScreeningResponse>("/screening/analyze", {
    method: "POST",
    body: {
      job_description: jobDescription,
      candidate_name: candidateName,
      candidate_id: candidateId,
    },
  });
}
