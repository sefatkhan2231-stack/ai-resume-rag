def validate_assessment(assessment: dict, analysis: dict) -> dict:
    """
    Post-filter the LLM's JSON output against the verified match results.
    The matching engine remains the source of truth -- if the model listed
    a skill under confirmed_strengths that isn't actually in our matched
    set (or vice versa for missing_requirements), drop it rather than
    trusting the model's free-text instruction-following.
    """
    matched = {
        r["skill"]
        for r in analysis["results"]
        if r["matched"]
    }

    missing = {
        r["skill"]
        for r in analysis["results"]
        if not r["matched"]
    }

    assessment["confirmed_strengths"] = [
        skill
        for skill in assessment.get("confirmed_strengths", [])
        if skill in matched
    ]

    assessment["missing_requirements"] = [
        skill
        for skill in assessment.get("missing_requirements", [])
        if skill in missing
    ]

    return assessment