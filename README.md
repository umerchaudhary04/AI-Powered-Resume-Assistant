# AI Resume Assistant

AI Resume Assistant is a Streamlit-based web application designed to help job seekers improve their resumes through transparent, criteria-based AI evaluation[cite: 1]. Instead of opaque "AI rewrites," this tool scores resumes against the established Harvard College Office of Career Services resume guide and generates specific, actionable improvements[cite: 1].

## Core Features

* **Document Parsing:** Extracts raw text and segments sections from uploaded PDF and DOCX files using `pdfplumber` and `python-docx`[cite: 1].
* **Harvard OCS Rubric Scoring:** Evaluates the resume on strict sub-criteria, including the use of strong action verbs, quantified impact metrics, consistent verb tenses, and the absence of first-person pronouns[cite: 1].
* **Job Description Matching:** Accepts an optional target job description to extract key requirements and flag missing skills or keywords in the user's resume[cite: 1].
* **Actionable Rewrite Suggestions:** Generates inline, section-by-section rewrite suggestions for weak bullet points, providing bracketed placeholders for missing metrics to ensure no factual content is fabricated[cite: 1].
* **Transparent Feedback:** Provides a structured breakdown of the overall score, the ratio of quantified metrics, and the reasoning behind every suggested change[cite: 1].

## Technology Stack

* **Language Model:** Google Gemini API (Flash/Flash-Lite models) for structured JSON evaluation and cost control[cite: 1].
* **Application Framework:** Streamlit (deployed via Streamlit Community Cloud)[cite: 1].
* **Development & Prototyping:** Google Colab (used for initial prompt design and parsing logic validation)[cite: 1].
* **Libraries:** `google-genai`, `pydantic`, `pdfplumber`, `python-docx`[cite: 1].

## Setup and Installation

**1. Clone the repository**

```bash
git clone https://github.com/yourusername/ai-resume-assistant.git
cd ai-resume-assistant

```

**2. Install dependencies**

```bash
pip install -r requirements.txt

```

**3. Configure the Gemini API Key**
For local development, create a `.streamlit/secrets.toml` file in the project root:

```toml
GEMINI_API_KEY = "your_actual_api_key_here"

```

**4. Run the application**

```bash
streamlit run app.py

```

## Project Scope and Constraints

This MVP is designed specifically for early-career job seekers and university students[cite: 1]. It intentionally excludes out-of-scope features such as job application tracking, cover letter generation, and visual template design[cite: 1]. To protect user privacy, uploaded files and extracted text are processed entirely in-memory and are not persisted beyond the active session[cite: 1].

**Owner:** Umer Asghar
**Version:** 1.0 (MVP)
