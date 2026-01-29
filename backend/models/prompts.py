PROMPT_TEMPLATE = """
You are an expert recruiter.

Resume:
{resume}

Job Description:
{jd}

Tasks:
1. Give match score out of 100
2. List missing skills
3. Suggest improvements
4. Rewrite 3 bullets better

Return STRICT JSON:

{{
 "score": int,
 "missing_skills": [],
 "suggestions": [],
 "rewritten_bullets": []
}}
"""
