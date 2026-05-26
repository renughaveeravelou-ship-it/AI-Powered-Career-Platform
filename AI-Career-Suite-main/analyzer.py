"""
analyzer.py - AI Resume Analysis
Supports all providers: NVIDIA Build, OpenRouter, OpenAI, Anthropic, Google Gemini,
Groq, DeepSeek, Mistral, Together AI, Perplexity, xAI, Cohere, HuggingFace
"""

import re
import json
import pdfplumber
from io import BytesIO
from providers import call_api, PROVIDERS


# ── Keep these for backward compat with app.py imports ──
FREE_MODELS  = PROVIDERS["OpenRouter"]["free_models"]
PAID_MODELS  = PROVIDERS["OpenRouter"]["paid_models"]
ALL_MODELS   = {**FREE_MODELS, **PAID_MODELS}


def get_model_id(display_name: str) -> str:
    return ALL_MODELS.get(display_name, display_name)


def extract_text_from_pdf(uploaded_file) -> str:
    text = ""
    try:
        uploaded_file.seek(0)
        with pdfplumber.open(BytesIO(uploaded_file.read())) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        raise ValueError(f"Could not read PDF: {str(e)}")
    if not text.strip():
        raise ValueError("No text found in PDF. Make sure it's not a scanned image.")
    return text.strip()


def analyze_resume(api_key: str, model_id: str, resume_text: str,
                   job_description: str, job_title: str = "",
                   company_name: str = "", provider_name: str = "OpenRouter") -> dict:

    prompt = f"""You are a senior technical recruiter and career coach with 15+ years at top MNC companies (Google, Amazon, Microsoft, TCS, Infosys). You deeply understand:
- How ATS systems (Workday, Greenhouse, Lever, Taleo) score resumes
- What hiring managers look for in 2025 tech candidates
- Real salary and hiring trends
- Why candidates get rejected at each stage

Analyze this resume against the job description with the precision of a real recruiter.

JOB TITLE: {job_title or "Not specified"}
COMPANY: {company_name or "Not specified"}

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Key recruiter insights to apply:
1. ATS rejects 75% of resumes — check exact keyword matches
2. Recruiters spend 6-7 seconds on first scan — check immediate visibility
3. Quantified achievements (numbers, %, $) are 40% more likely to pass
4. Skills listed but not demonstrated in experience are red flags
5. GitHub/portfolio links dramatically increase callbacks for tech roles
6. F1 visa/OPT/CPT mention matters for US companies
7. Cloud certifications (AWS, GCP, Azure) boost tech resume scores significantly
8. Buzzwords without context waste valuable resume space

Provide ONLY valid JSON (no markdown, no extra text):
{{
  "ats_score": <integer 0-100>,
  "match_score": <integer 0-100>,
  "hire_probability": <integer 0-100, realistic interview callback chance>,
  "matched_skills": [<skills in BOTH resume and JD>],
  "missing_skills": [<critical JD skills absent from resume>],
  "strengths": [<3-5 genuine strengths with specific resume evidence>],
  "improvements": [<4-6 specific improvements with exact wording suggestions>],
  "keyword_suggestions": [<6-8 exact ATS keywords from the JD to add>],
  "experience_gap": "<honest assessment of experience level match>",
  "education_match": "<education requirements match assessment>",
  "red_flags": [<1-3 things a recruiter notices negatively — be honest>],
  "overall_summary": "<2-3 sentences honest assessment, mention visa/OPT if F1 relevant>",
  "quick_wins": [<3 things to fix TODAY to immediately improve callback rate>],
  "salary_insight": "<estimated salary range this resume would command>"
}}

Be brutally honest — candidates need truth, not false hope."""

    try:
        raw = call_api(provider_name, api_key, model_id, prompt, temperature=0.3, max_tokens=2000)

        # Strip markdown code fences
        raw = re.sub(r"^```json\s*", "", raw)
        raw = re.sub(r"^```\s*",     "", raw)
        raw = re.sub(r"\s*```$",     "", raw)

        # Extract JSON object
        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
        if json_match:
            raw = json_match.group()

        result = json.loads(raw)

        defaults = {
            "ats_score": 0, "match_score": 0, "hire_probability": 0,
            "matched_skills": [], "missing_skills": [], "strengths": [],
            "improvements": [], "keyword_suggestions": [], "experience_gap": "",
            "education_match": "", "overall_summary": "", "quick_wins": [],
            "red_flags": [], "salary_insight": ""
        }
        for key, default in defaults.items():
            result.setdefault(key, default)

        result["ats_score"]        = max(0, min(100, int(result["ats_score"])))
        result["match_score"]      = max(0, min(100, int(result["match_score"])))
        result["hire_probability"] = max(0, min(100, int(result["hire_probability"])))
        return result

    except json.JSONDecodeError:
        raise ValueError("AI returned invalid response. Try again or switch model.")
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Analysis failed: {str(e)}")


def get_score_color(score: int) -> str:
    if score >= 75: return "#00C851"
    elif score >= 50: return "#ffbb33"
    else: return "#ff4444"


def get_score_label(score: int) -> str:
    if score >= 80: return "Excellent"
    elif score >= 65: return "Good"
    elif score >= 50: return "Fair"
    else: return "Needs Work"