import json

from backend.app.llm.assessment import generate_candidate_assessment
from backend.app.llm.validation import validate_assessment
from backend.app.screening.requirements import extract_job_requirements, flatten_requirements
from backend.app.screening.scoring import analyze_requirements
from backend.app.screening.screening import build_candidate_prompt, print_candidate_report


job_description = """
Machine Learning Engineer Intern

Requirements:
- Strong Python programming skills
- Knowledge of machine learning algorithms
- Experience with scikit-learn
- Knowledge of NLP and Transformers
- Experience with PyTorch or TensorFlow
- Knowledge of SQL databases
- Good problem solving skills
- Experience working with Git and GitHub
"""

requirements = extract_job_requirements(job_description)
flat_requirements = flatten_requirements(requirements)
print(flat_requirements)

analysis = analyze_requirements(flat_requirements)
print_candidate_report(analysis)

prompt = build_candidate_prompt(analysis)

assessment = generate_candidate_assessment(prompt)

assessment = validate_assessment(
    assessment,
    analysis
)

print(json.dumps(assessment, indent=2))