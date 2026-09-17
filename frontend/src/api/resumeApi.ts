import type {
  BatchUploadResponse,
  RankResponse,
  ResumeUploadResponse,
} from "../types";
import request from "./client";

export function uploadResume(file: File): Promise<ResumeUploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  return request<ResumeUploadResponse>("/resumes/upload", {
    method: "POST",
    body: formData,
  });
}

export function uploadResumes(files: File[]): Promise<BatchUploadResponse> {
  const formData = new FormData();
  files.forEach((file) => formData.append("files", file));

  return request<BatchUploadResponse>("/resumes/batch-upload", {
    method: "POST",
    body: formData,
  });
}

export function rankCandidates(
  jobDescription: string,
  candidateIds: string[],
): Promise<RankResponse> {
  return request<RankResponse>("/resumes/rank", {
    method: "POST",
    body: {
      job_description: jobDescription,
      candidate_ids: candidateIds,
    },
  });
}
