from backend.app.screening.requirements import extract_job_requirements, flatten_requirements


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