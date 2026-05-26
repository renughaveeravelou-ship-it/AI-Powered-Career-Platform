"""
job_matching.py - Job matching and discovery engine.
Calculates keyword similarity and identifies gaps between candidate resumes and job requirements.
"""

import json
import re


def match_resume_to_jobs(resume_text: str, jobs: list) -> list:
    """
    Compares candidate resume text against the vacancies in the database.
    Calculates overlap scores and matches skills, returning a sorted list.
    """
    if not resume_text or not jobs:
        return []
        
    resume_lower = resume_text.lower()
    matches = []
    
    for job in jobs:
        req_skills = job.get("required_skills", [])
        matched = []
        missing = []
        
        for skill in req_skills:
            # Create regex boundary match to avoid partial word substring errors
            # (e.g. matching "Go" inside "Google")
            skill_escaped = re.escape(skill.lower())
            pattern = rf"\b{skill_escaped}\b"
            if re.search(pattern, resume_lower):
                matched.append(skill)
            else:
                # Direct fallback substring search for multi-word skills like "Machine Learning"
                if len(skill_escaped.split()) > 1 and skill_escaped in resume_lower:
                    matched.append(skill)
                else:
                    missing.append(skill)
                    
        total_skills = len(req_skills)
        if total_skills > 0:
            score = round((len(matched) / total_skills) * 100)
        else:
            score = 0
            
        # Calculate a slight boost if job title keywords appear in resume
        title_keywords = job.get("title", "").lower().split()
        title_hits = 0
        for word in title_keywords:
            if len(word) > 2 and word in resume_lower:
                title_hits += 1
        if title_hits > 0:
            score = min(100, score + (title_hits * 5))
            
        matches.append({
            "job_id": job.get("id"),
            "title": job.get("title"),
            "company": job.get("company"),
            "location": job.get("location", "Remote"),
            "salary_range": job.get("salary_range", "N/A"),
            "score": score,
            "matched_skills": matched,
            "missing_skills": missing,
            "description": job.get("description", "")
        })
        
    # Sort matches by score descending
    return sorted(matches, key=lambda x: x["score"], reverse=True)
