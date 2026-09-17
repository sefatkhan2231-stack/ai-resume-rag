import { Route, Routes } from "react-router-dom";
import AppLayout from "./layouts/AppLayout";
import DashboardPage from "./pages/DashboardPage";
import JobMatchingPage from "./pages/JobMatchingPage";
import ResumeScreeningPage from "./pages/ResumeScreeningPage";
import ScreeningHistoryPage from "./pages/ScreeningHistoryPage";

export default function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<DashboardPage />} />
        <Route path="resume-screening" element={<ResumeScreeningPage />} />
        <Route path="job-matching" element={<JobMatchingPage />} />
        <Route path="screening-history" element={<ScreeningHistoryPage />} />
      </Route>
    </Routes>
  );
}
