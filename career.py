"""
career.py - AI-powered career path recommendation engine.
Generates tailored career roadmap options and plots salary growth benchmarks.
"""

import re
import json
import plotly.express as px
import plotly.graph_objects as go
from providers import call_api


def recommend_career_path(skills: list, interests: str, salary_goal: str,
                          provider: str, api_key: str, model_id: str) -> list:
    """
    Asks the AI dispatcher to recommend 3 suitable career paths.
    """
    skills_str = ", ".join(skills) if skills else "Not specified"
    prompt = f"""You are an elite career strategist. Analyze the user's skillset and career interest and recommend 3 tailored career paths.

USER SKILLS: {skills_str}
USER INTERESTS: {interests}
TARGET SALARY GOAL: {salary_goal}

Provide exactly 3 distinct recommendations in JSON format (do not return any markdown code fences, just raw JSON).
The response MUST follow this exact schema:
[
  {{
    "title": "<career path title, e.g., Senior Data Engineer>",
    "average_salary": <integer representing annual salary in USD, e.g., 145000>,
    "description": "<2-3 sentence overview of what they do>",
    "growth_rate": <integer 0-100 indicating projected 10-year job demand/growth>,
    "roadmap_steps": [
      "<step 1, e.g., Master Apache Spark and cloud databases>",
      "<step 2, e.g., Earn AWS Data Analytics specialty certification>",
      "<step 3, e.g., Build 2 production-grade pipeline portfolio projects>"
    ],
    "matching_score": <integer 0-100 indicating match quality based on current skills>
  }}
]
"""
    try:
        raw = call_api(provider, api_key, model_id, prompt, temperature=0.4, max_tokens=1500)
        
        # Strip markdown fences
        raw = re.sub(r"^```json\s*", "", raw)
        raw = re.sub(r"^```\s*",     "", raw)
        raw = re.sub(r"\s*```$",     "", raw)

        json_match = re.search(r'\[.*\]', raw, re.DOTALL)
        if json_match:
            raw = json_match.group()

        result = json.loads(raw)
        
        # Verify schema is list of 3 dicts
        if not isinstance(result, list):
            result = [result]
            
        defaults = {
            "title": "N/A", "average_salary": 80000, 
            "description": "No description available", "growth_rate": 50,
            "roadmap_steps": [], "matching_score": 50
        }
        for item in result:
            for k, v in defaults.items():
                item.setdefault(k, v)
        return result[:3]
    except Exception as e:
        raise ValueError(f"AI recommendations failed: {str(e)}")


def plot_career_salaries(paths: list):
    """
    Plots a glowing Plotly bar chart comparing recommended career path salaries.
    """
    titles = [p["title"] for p in paths]
    salaries = [p["average_salary"] for p in paths]
    growth = [p["growth_rate"] for p in paths]
    
    fig = go.Figure()
    
    # Add Bar chart for Salary
    fig.add_trace(go.Bar(
        x=titles,
        y=salaries,
        name="Median Salary ($)",
        marker=dict(
            color='rgba(139, 92, 246, 0.65)',
            line=dict(color='rgb(139, 92, 246)', width=1.5)
        ),
        text=[f"${s:,}" for s in salaries],
        textposition='auto',
        hoverinfo='y+name'
    ))
    
    # Add Line trace for Growth rate % on secondary axis
    fig.add_trace(go.Scatter(
        x=titles,
        y=[g * 1500 for g in growth], # scale for visibility
        name="10-Year Growth Rate (%)",
        mode='lines+markers',
        line=dict(color='rgb(6, 182, 212)', width=3),
        marker=dict(size=10, color='rgb(236, 72, 153)'),
        hovertext=[f"{g}% Growth" for g in growth],
        hoverinfo='text+name'
    ))

    fig.update_layout(
        title=dict(text="Recommended Career Paths Analysis", font=dict(color="#ffffff")),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        yaxis=dict(
            title="Salary Range ($)",
            gridcolor='rgba(255, 255, 255, 0.05)',
            zerolinecolor='rgba(255, 255, 255, 0.05)'
        ),
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig
