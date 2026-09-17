from app.llm.assessment import generate_candidate_assessment
from app.llm.validation import validate_assessment
from app.screening.requirements import extract_job_requirements, flatten_requirements
from app.screening.scoring import analyze_requirements
from app.screening.screening import build_candidate_prompt


def get_job_requirements(job_description: str) -> dict:
    requirements = extract_job_requirements(job_description)
    flattened = flatten_requirements(requirements)
    return {"requirements": requirements, "flattened": flattened}


def screen_candidate(job_description: str, candidate_id: str = None, candidate_name: str = "Candidate") -> dict:

    requirements = extract_job_requirements(job_description)
    flat_requirements = flatten_requirements(requirements)

    analysis = analyze_requirements(flat_requirements, candidate_id=candidate_id)

    prompt = build_candidate_prompt(analysis)
    assessment = generate_candidate_assessment(prompt)
    assessment = validate_assessment(assessment, analysis)

    skills = {result["skill"]: result["matched"] for result in analysis["results"]}

    evidence = []
    for result in analysis["matched"]:
        for item in result["evidence"]:
            evidence.append({"skill": result["skill"], "text": item["document"]})

    return {
        "candidate": candidate_name,
        "score": analysis["score"],
        "skills": skills,
        "missing_skills": [result["skill"] for result in analysis["missing"]],
        "evidence": evidence,
        "overall_assessment": assessment.get("overall_assessment", ""),
        "final_recommendation": assessment.get("final_recommendation", ""),
    }