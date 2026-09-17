from app.screening.verification import check_skill


def check_requirements(requirements, candidate_id: str = None):

    results = []

    for requirement in requirements:
        result = check_skill(requirement, candidate_id=candidate_id)
        results.append(result)

    return results


def calculate_match_score(results: list) -> float:
    if not results:
        return 0.0

    matched = sum(
        result["matched"]
        for result in results
    )

    return round(
        matched / len(results) * 100,
        2
    )


def build_match_report(requirements: list, candidate_id: str = None) -> dict:
    results = check_requirements(requirements, candidate_id=candidate_id)

    score = calculate_match_score(results)

    matched = [
        result for result in results
        if result["matched"]
    ]

    missing = [
        result for result in results
        if not result["matched"]
    ]

    return {
        "score": score,
        "results": results,
        "matched": matched,
        "missing": missing
    }

def analyze_requirements(requirements: list, candidate_id: str = None) -> dict:
    return build_match_report(requirements, candidate_id=candidate_id)


def _recommendation_for(score: float) -> str:

    if score >= 80:
        return "Strong Match"
    if score >= 55:
        return "Good Match"
    if score >= 30:
        return "Partial Match"
    return "Weak Match"