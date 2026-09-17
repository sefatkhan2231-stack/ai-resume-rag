import type { JobMatchingResponse } from "../types";
import request from "./client";

export function analyzeJobMatching(
  jobDescription: string,
  candidateIds: string[],
): Promise<JobMatchingResponse> {
  return request<JobMatchingResponse>("/job-matching/analyze", {
    method: "POST",
    body: { job_description: jobDescription, candidate_ids: candidateIds },
  });
}
