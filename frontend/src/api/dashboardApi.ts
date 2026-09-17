import type {
  ActivityPoint,
  DashboardStats,
  ScreeningHistoryItem,
} from "../types";
import request from "./client";

export function getDashboardStats(): Promise<DashboardStats> {
  return request<DashboardStats>("/dashboard/stats");
}

export function getDashboardActivity(days = 30): Promise<ActivityPoint[]> {
  return request<ActivityPoint[]>(`/dashboard/activity?days=${days}`);
}

export function getScreeningHistory(
  limit = 50,
): Promise<ScreeningHistoryItem[]> {
  return request<ScreeningHistoryItem[]>(`/dashboard/history?limit=${limit}`);
}
