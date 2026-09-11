from google import genai
from google.genai import types
from pydantic import BaseModel, Field

class CriterionScore(BaseModel):
    criterion_name: str = Field(description="Rubric aspect name (e.g., Action Verbs, Formatting)")
    score: int = Field(description="Score from 0 to 10")
    feedback: str = Field(description="Critique based on Harvard OCS standards")

class RewriteSuggestion(BaseModel):
    section: str = Field(description="Resume section")
    original_text: str = Field(description="Weak phrase")
    suggested_text: str = Field(description="Rewritten version with placeholders like [X%]")
    improvement_reason: str = Field(description="Reason for improvement")

class ResumeAnalysisResult(BaseModel):
    overall_score: int
    quantified_impact_ratio: str
    sub_scores: list[CriterionScore]
    missing_jd_keywords: list[str] = []
    suggestions: list[RewriteSuggestion]

SYSTEM_PROMPT = """
You are an expert resume evaluator using the Harvard College OCS resume guide:
1. Strong action verbs (no weak words like 'helped').
2. Quantified impact metrics.
3. Consistent verb tenses.
4. No first-person pronouns (I, me).
Output JSON strictly adhering to the schema. Do not invent facts.
"""

def analyze_resume(api_key: str, resume_text: str, job_description: str = "") -> ResumeAnalysisResult:
    client = genai.Client(api_key=API_KEY)
    prompt = f"Resume:\n{resume_text}\n"
    if job_description.strip():
        prompt += f"\nJob Description:\n{job_description}\nExtract missing keywords."

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=ResumeAnalysisResult,
            temperature=0.2,
        ),
    )
    return ResumeAnalysisResult.model_validate_json(response.text)
