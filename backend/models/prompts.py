# backend/models/prompts.py
PROMPT_TEMPLATE = """Analyze this resume against the job description and provide a detailed evaluation.

RESUME:
{resume}

JOB DESCRIPTION:
{jd}

Provide your analysis in the following JSON format:
{{
    "score": <number 0-100>,
    "missing_skills": [<list of 3-5 key skills the candidate is missing>],
    "suggestions": [<list of 3-5 specific improvements for the resume>],
    "rewritten_bullets": [<3 rewritten resume bullet points that better match the job description>]
}}

Requirements:
- Score should reflect how well the resume matches the job (0-100)
- Missing skills should be specific technical or soft skills mentioned in the JD
- Suggestions should be actionable improvements
- Rewritten bullets should use strong action verbs and quantify achievements when possible

Return ONLY the JSON object, no other text."""