import re

from app.rag.retrieval import retrieve_and_rerank
from app.services.llm_service import generate

ALIASES = {
    "python programming": "Python",
    "python programming skills": "Python",
    "sql databases": "SQL",
    "sql database": "SQL",
    "sql/database knowledge": "SQL",
    "experience working with git and github": "Git and GitHub",
    "good problem solving skills": "Problem solving",
}

SUBSTRING_OK = {}


def normalize_requirement(requirement: str) -> str:
    key = requirement.strip().lower()
    return ALIASES.get(key, requirement)


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\- ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _term_matches(term: str, evidence: str) -> bool:
    if re.search(rf"\b{re.escape(term)}\b", evidence):
        return True
    for allowed_word in SUBSTRING_OK.get(term, []):
        if allowed_word in evidence:
            return True
    return False


def exact_skill_match(skill: str, evidence_text: str) -> bool:
    skill_terms = re.findall(r"[a-z0-9+#.-]+", skill.lower())
    evidence_norm = normalize_text(evidence_text)
    return all(_term_matches(term, evidence_norm) for term in skill_terms)


def verify_skill_llm(skill: str, evidence_text: str) -> bool:

    prompt = f"""
You are a strict resume evidence verifier.

Requirement:
{skill}

Resume evidence:
{evidence_text}

Determine whether the resume evidence explicitly supports
the requirement.

Rules:

1. Return TRUE only when the requirement itself is explicitly
   mentioned or the evidence is an unmistakable direct statement
   of experience with that requirement.

2. Do NOT infer related skills.

3. Python does NOT imply machine learning.

4. Python does NOT imply scikit-learn.

5. MySQL does NOT imply SQL unless SQL is explicitly mentioned.

6. Git does NOT imply GitHub.

7. Transformers do NOT imply NLP.

8. A general programming language does not imply a framework,
   library, algorithm, or domain.

9. If uncertain, return FALSE.

Return ONLY:
TRUE
or
FALSE
"""
    response = generate(
        system_prompt="Return only TRUE or FALSE.",
        user_prompt=prompt,
    )
    answer = response.strip().upper()
    return answer == "TRUE"


def select_best_evidence(evidence, max_results=2):
    """
    Keep only the strongest verified evidence.
    Prefer exact/stronger reranker matches.

    Without this, check_skill can return every chunk that happened to pass
    verification (e.g. ABOUT ME, SKILLS, and PROJECTS all mentioning
    "frontend"), which makes reports noisy and non-deterministic in ordering.
    """
    if not evidence:
        return []

    sorted_evidence = sorted(
        evidence,
        key=lambda x: x.get("rerank_score", float("-inf")),
        reverse=True
    )

    return sorted_evidence[:max_results]


def check_skill(skill: str, candidate_id: str = None) -> dict:
    original_skill = skill
    normalized_skill = normalize_requirement(skill)

    print(normalized_skill)

    query = normalized_skill
    evidence = retrieve_and_rerank(query, candidate_id=candidate_id)

    if not evidence:
        return {"skill": original_skill, "normalized_skill": normalized_skill, "matched": False, "evidence": []}

    evidence = select_best_evidence(evidence, max_results=1)

    verified_evidence = []

    for item in evidence:
        document = item["document"]

        if exact_skill_match(normalized_skill, document):
            verified_evidence.append(item)
            print(verified_evidence)
            continue

        if verify_skill_llm(normalized_skill, document):
            verified_evidence.append(item)
            print(verified_evidence)

    return {
        "skill": original_skill,
        "normalized_skill": normalized_skill,
        "matched": True,
        "evidence": evidence
    }
