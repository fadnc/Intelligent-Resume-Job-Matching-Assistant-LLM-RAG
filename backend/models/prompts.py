# backend/models/prompts.py
PROMPT_TEMPLATE = """Score this resume for the job (0-100). List 2-3 missing skills and suggestions. Return JSON only.

Resume: {resume}

Job: {jd}

JSON: {{"score": 0, "missing_skills": [], "suggestions": [], "rewritten_bullets": []}}"""