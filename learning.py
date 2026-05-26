"""
learning.py - AI-powered learning path assistant.
Generates week-by-week study roadmaps for missing skills and matches with courses.
"""

from providers import call_api
import urllib.parse


def generate_study_guide(skill: str, provider: str, api_key: str, model_id: str) -> str:
    """
    Generates an automated study curriculum guide for a specific skill.
    """
    prompt = f"""You are an expert technical instructor and educator. 
Create a detailed, week-by-week study curriculum for the skill: "{skill}".

Structure your output into 4 weeks:
- WEEK 1: Core Concepts & Foundational Theory
- WEEK 2: Practical Exercises & Tooling Setup
- WEEK 3: Intermediate Tasks & Cloud Integration
- WEEK 4: Capstone Portfolio Project

For each week, define:
1. Learning Objective
2. Key Topics to Master
3. Practical Exercise / Lab to perform
4. Recommended documentation links/references

Keep the language encouraging, professional, and clear. Format the output in Markdown with clean headers and bullet points.
"""
    try:
        raw = call_api(provider, api_key, model_id, prompt, temperature=0.5, max_tokens=1500)
        return raw
    except Exception as e:
        raise ValueError(f"AI Study Guide failed: {str(e)}")


def get_course_search_links(skill: str) -> dict:
    """
    Generates links to search queries for Udemy, Coursera, and YouTube.
    """
    encoded_query = urllib.parse.quote(skill)
    return {
        "Udemy": f"https://www.udemy.com/courses/search/?q={encoded_query}",
        "Coursera": f"https://www.coursera.org/search?query={encoded_query}",
        "YouTube": f"https://www.youtube.com/results?search_query={encoded_query}+tutorial"
    }
