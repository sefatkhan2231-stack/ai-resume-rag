import json

def print_candidate_report(analysis: dict):
    print("=" * 60)
    print("AI RESUME SCREENING REPORT")
    print("=" * 60)
    print(f"\nMATCH SCORE: {analysis['score']:.2f}%")

    print("\nMATCHED")
    print("-" * 60)
    for result in analysis["results"]:
        if not result["matched"]:
            continue
        print(f"\n\u2713 {result['skill']}")
        for evidence in result["evidence"]:
            section = evidence["metadata"].get("section")
            subsection = evidence["metadata"].get("subsection")
            print(f"  Source: {section} \u2192 {subsection}")
            print(f"  Evidence: {evidence['document']}")

    print("\nMISSING")
    print("-" * 60)
    for result in analysis["results"]:
        if result["matched"]:
            continue
        print(f"\n\u2717 {result['skill']}")
        print("  No supporting evidence found in the resume.")


def build_evidence_context(analysis: dict) -> str:
    grouped = {}
    for result in analysis["results"]:
        if not result["matched"]:
            continue
        skill = result["skill"]
        grouped.setdefault(skill, [])
        for evidence in result["evidence"]:
            metadata = evidence["metadata"]
            item = (metadata.get("section"), metadata.get("subsection"), evidence["document"])
            if item not in grouped[skill]:
                grouped[skill].append(item)

    parts = []
    for skill, evidence_list in grouped.items():
        block = f"Requirement: {skill}\n"
        for section, subsection, document in evidence_list:
            block += f"\nSource: {section} \u2192 {subsection}\nEvidence:\n{document}\n"
        parts.append(block)
    return "\n".join(parts)


def build_candidate_prompt(analysis: dict) -> str:

    matched = [
        r["skill"]
        for r in analysis["results"]
        if r["matched"]
    ]

    missing = [
        r["skill"]
        for r in analysis["results"]
        if not r["matched"]
    ]

    return f"""
Analyze ONLY these verified job requirements.

MATCH SCORE:
{analysis['score']:.2f}%

MATCHED REQUIREMENTS:
{json.dumps(matched)}

MISSING REQUIREMENTS:
{json.dumps(missing)}

Return ONLY this JSON structure:

{{
    "overall_assessment": "",
    "confirmed_strengths": [],
    "missing_requirements": [],
    "final_recommendation": ""
}}

Rules:

- confirmed_strengths MUST contain only matched requirements.
- missing_requirements MUST contain only missing requirements.
- Do not mention any other resume skill.
- Do not mention React unless it appears in MATCHED REQUIREMENTS.
- Do not mention Laravel unless it appears in MATCHED REQUIREMENTS.
- Python does not imply machine learning.
- Python does not imply scikit-learn.
- Python does not imply NLP.
- MySQL does not imply SQL.
- Transformers do not imply NLP.
- Missing evidence must remain missing.
- If uncertain, say that the requirement is not verified.
- Do not recommend another job role.
- Do not invent experience.

"""