"""
portfolio.py - AI-powered personal portfolio website compiler.
Integrates with the public GitHub API to extract programming language breakdowns and repository metrics.
"""

import requests
import json
import re
from providers import call_api


def fetch_github_profile_data(username: str) -> dict:
    """
    Fetches public repositories for a user and calculates language distribution.
    Uses public endpoint (no key required for low-volume requests).
    """
    url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
    try:
        res = requests.get(url, headers={"User-Agent": "AI-Career-Platform"}, timeout=8)
        if res.status_code != 200:
            return {"error": f"GitHub user not found or API limit reached. (HTTP {res.status_code})"}
        
        repos = res.json()
        if not repos or not isinstance(repos, list):
            return {"languages": {}, "top_repos": []}
            
        languages = {}
        top_repos = []
        
        # Sort repos by stars + forks to find top ones
        sorted_repos = sorted(repos, key=lambda r: (r.get("stargazers_count", 0) + r.get("forks_count", 0)), reverse=True)
        
        for r in sorted_repos[:5]:
            top_repos.append({
                "name": r.get("name", ""),
                "description": r.get("description", "No description provided."),
                "stars": r.get("stargazers_count", 0),
                "forks": r.get("forks_count", 0),
                "url": r.get("html_url", ""),
                "language": r.get("language", "")
            })
            
        # Count language distribution
        total_size = 0
        for r in repos:
            lang = r.get("language")
            if lang:
                # Give each repo language a weight of 1, or use language sizes (requires sub-queries, so simpler weighting here)
                languages[lang] = languages.get(lang, 0) + 1
                total_size += 1
                
        # Turn to percentages
        lang_percentages = {}
        if total_size > 0:
            for k, v in languages.items():
                lang_percentages[k] = round((v / total_size) * 100, 1)
                
        return {
            "languages": lang_percentages,
            "top_repos": top_repos
        }
    except Exception as e:
        return {"error": f"Failed to connect to GitHub API: {str(e)}"}


def compile_portfolio_code(profile: dict, theme: str, provider: str, 
                           api_key: str, model_id: str) -> str:
    """
    Compiles a self-contained responsive HTML/CSS file representing the portfolio.
    """
    github_data_str = json.dumps(profile.get("github_data", {}), indent=2)
    skills_str = ", ".join(profile.get("skills", []))
    
    prompt = f"""You are a master web designer and frontend engineer.
Compile a fully responsive, self-contained personal portfolio website (HTML, CSS within <style>, and interactive JavaScript code) for:

NAME: {profile.get('name', 'Career Candidate')}
TITLE: {profile.get('title', 'Software Developer')}
BIO: {profile.get('bio', 'Aspiring tech professional.')}
SKILLS: {skills_str}
THEME STYLE: {theme}
GITHUB STATS:
{github_data_str}

Theme Specifications:
- Minimalist: Crisp modern typography (e.g. Inter), white/light gray background, dark text, clean borders, minimal decoration.
- Cyberpunk: Dark background (#05050d), neon pink (#ff007f) and cyan (#00f3ff) glowing borders, grid lines, terminal style.
- Dark Luxury: Deep purple and indigo space background, semi-transparent frosted-glass containers (glassmorphism), gold highlights, subtle transitions.

Features to include:
1. Header / Navbar with smooth hover navigation links (Home, Skills, Projects, Contact).
2. Hero section with responsive text layout, social links.
3. Skills dashboard displaying the GitHub programming language split (e.g., in a styled progress bar or pie-chart-like flex box layout).
4. Top Projects grid showing the repositories listed in GITHUB STATS.
5. Interactive contact form (just client-side layout and success alerts).
6. Complete responsive styling so it looks premium on both mobile and desktop.

Return ONLY the complete HTML file contents, starting with <!DOCTYPE html> and ending with </html>. 
No Markdown wrapper blocks, no extra conversational text outside the HTML. Output valid web code.
"""
    try:
        raw = call_api(provider, api_key, model_id, prompt, temperature=0.5, max_tokens=3000)
        
        # Clean any accidental code fences from AI
        raw = re.sub(r"^```html\s*", "", raw)
        raw = re.sub(r"^```\s*",     "", raw)
        raw = re.sub(r"\s*```$",     "", raw)
        
        return raw.strip()
    except Exception as e:
        raise ValueError(f"Portfolio generation failed: {str(e)}")
