import json

from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.models.screening import ScreeningRecord
from app.screening.requirements import extract_job_requirements, flatten_requirements
from app.screening.scoring import analyze_requirements, _recommendation_for
from app.screening.screening import build_candidate_prompt
from app.llm.assessment import generate_candidate_assessment
from app.llm.validation import validate_assessment


def analyze_job_matching(
    job_description: str, db: Session, candidate_ids: list[str] | None = None
) -> dict:

    query = db.query(Candidate)
    if candidate_ids:
        query = query.filter(Candidate.candidate_id.in_(candidate_ids))
    candidates = query.order_by(Candidate.created_at.desc()).all()

    if not candidates:
        return {"results": [], "average_score": 0.0, "screening_id": None}

    requirements = extract_job_requirements(job_description)
    flat_requirements = flatten_requirements(requirements)

    results = []
    for candidate in candidates:
        analysis = analyze_requirements(flat_requirements, candidate_id=candidate.candidate_id)

        prompt = build_candidate_prompt(analysis)
        assessment = generate_candidate_assessment(prompt)
        assessment = validate_assessment(assessment, analysis)

        evidence = []
        for result in analysis["matched"]:
            for item in result["evidence"]:
                evidence.append({"skill": result["skill"], "text": item["document"]})

        results.append(
            {
                "candidate_id": candidate.candidate_id,
                "resume_id": candidate.resume_id,
                "name": candidate.name or candidate.filename,
                "email": candidate.email,
                "phone": candidate.phone,
                "score": analysis["score"],
                "matched_skills": [r["skill"] for r in analysis["matched"]],
                "missing_skills": [r["skill"] for r in analysis["missing"]],
                "strengths": assessment.get("confirmed_strengths", []),
                "gaps": assessment.get("missing_requirements", []),
                "evidence": evidence,
                "overall_assessment": assessment.get("overall_assessment", ""),
                "final_recommendation": assessment.get("final_recommendation", ""),
                "recommendation": _recommendation_for(analysis["score"]),
            }
        )

    results.sort(key=lambda r: r["score"], reverse=True)
    for i, result in enumerate(results, start=1):
        result["rank"] = i

    average_score = round(sum(r["score"] for r in results) / len(results), 2)

    record = ScreeningRecord(
        screening_type="job_matching",
        number_of_resumes=len(results),
        job_description=job_description,
        average_score=average_score,
        results_json=json.dumps(results),
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {"results": results, "average_score": average_score, "screening_id": record.id}