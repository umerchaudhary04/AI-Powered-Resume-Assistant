import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

class CriterionScore(BaseModel):
    criterion_name: str = Field(description="Rubric aspect name (e.g., Action Verbs, Quantified Impact, Verb Tense, Structure)")
    score: int = Field(description="Score from 0 to 10")
    feedback: str = Field(description="Concrete critique based on Harvard OCS resume standards")

class RewriteSuggestion(BaseModel):
    section: str = Field(description="The resume section containing the text")
    original_text: str = Field(description="The weak phrase or bullet point")
    suggested_text: str = Field(description="Rewritten version preserving factual truth with placeholders for missing metrics")
    improvement_reason: str = Field(description="Explanation of what makes this version stronger")

class ResumeAnalysisResult(BaseModel):
    overall_score: int = Field(description="Weighted overall score out of 100")
    quantified_impact_ratio: str = Field(description="e.g., '3/10 bullets contain metrics'")
    sub_scores: list[CriterionScore]
    missing_jd_keywords: list[str] = Field(default_factory=list, description="Keywords present in JD but missing in resume")
    suggestions: list[RewriteSuggestion]

SYSTEM_PROMPT = """
You are an expert resume evaluator applying strict criteria from the Harvard College Office of Career Services resume guide:
1. Bullets must begin with strong, varied action verbs (e.g., 'Spearheaded', 'Engineered', not 'Helped' or 'Responsible for').
2. Quantified impact must be present (%, $, numbers, user scale).
3. Consistent verb tenses (past roles = past tense; current roles = present tense).
4. Strictly zero first-person pronouns (I, me, my, we).
5. Appropriate brevity and reverse-chronological order.

Never invent metrics or facts. When improving bullet points, use bracketed placeholders like [X%] or [$Y] for values the user must supply.
"""

def analyze_resume(api_key: str, resume_text: str, job_description: str = "") -> ResumeAnalysisResult:
    client = genai.Client(api_key=api_key)
    
    prompt = f"Resume Content:\n{resume_text}\n"
    if job_description.strip():
        prompt += f"\nTarget Job Description:\n{job_description}\n"
        prompt += "\nEvaluate relevance to the target job description and extract missing keywords/skills."

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=ResumeAnalysisResult,
            temperature=0.2,
        ),
    )
    return ResumeAnalysisResult.model_validate_json(response.text)
