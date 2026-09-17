import csv
import io
import json

from app.models.screening import ScreeningRecord


def _join(items: list[str]) -> str:
    return "; ".join(items)


def _build_ranking_csv(results: list[dict]) -> str:

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        ["Rank", "Candidate", "Email", "Phone", "Matched Skills", "Missing Skills", "Match Score", "Recommendation"]
    )
    for r in results:
        writer.writerow(
            [
                r["rank"],
                r["name"],
                r.get("email") or "",
                r.get("phone") or "",
                _join(r["matched_skills"]),
                _join(r["missing_skills"]),
                r["score"],
                r["recommendation"],
            ]
        )
    return buffer.getvalue()


def _build_job_matching_csv(results: list[dict]) -> str:

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        ["Rank", "Candidate", "Email", "Skills Match (%)", "Strengths", "Gaps", "Recommendation"]
    )
    for r in results:
        writer.writerow(
            [
                r["rank"],
                r["name"],
                r.get("email") or "",
                r["score"],
                _join(r["strengths"]),
                _join(r["gaps"]),
                r["recommendation"],
            ]
        )
    return buffer.getvalue()


def build_export(record: ScreeningRecord) -> tuple[str, str]:

    results = json.loads(record.results_json)
    date_str = record.created_at.strftime("%Y-%m-%d")

    if record.screening_type == "job_matching":
        csv_text = _build_job_matching_csv(results)
        filename = f"job-matching-results-{date_str}.csv"
    else:
        csv_text = _build_ranking_csv(results)
        filename = f"resume-screening-results-{date_str}.csv"

    return csv_text, filename