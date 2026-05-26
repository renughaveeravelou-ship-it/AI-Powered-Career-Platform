"""
gamification.py - Tracks achievements, streaks, badges, and XP points for user profiles.
"""

import sqlite3
import json
from datetime import datetime
from database import DB_PATH, add_user_xp, update_user_badges, get_user_by_id

# Badge Definitions with Descriptions and Icons
BADGES = {
    "ATS Apprentice": {
        "description": "Analyze your first resume to establish a baseline.",
        "icon": "📝",
        "criteria": "Completed 1 resume analysis"
    },
    "ATS Master": {
        "description": "Score 80+ ATS score on any resume analysis.",
        "icon": "🏆",
        "criteria": "ATS Score >= 80"
    },
    "Interview Ready": {
        "description": "Generate custom interview preparation questions.",
        "icon": "🎤",
        "criteria": "Run Interview Prep generator"
    },
    "Continuous Learner": {
        "description": "Build a customized study roadmap using AI Learning Assistant.",
        "icon": "📚",
        "criteria": "Generate 1 study guide"
    },
    "Web Artisan": {
        "description": "Generate a professional HTML/CSS portfolio using AI.",
        "icon": "💻",
        "criteria": "Compile 1 portfolio template"
    },
    "Streak Master": {
        "description": "Maintain a daily platform activity streak of 3+ days.",
        "icon": "🔥",
        "criteria": "Streak >= 3 days"
    }
}


def evaluate_badges(user_id: int) -> list:
    """
    Examines database state to see what badges the user qualifies for.
    Returns the list of unlocked badge names.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    unlocked = []

    # Get user stats
    cursor.execute("SELECT streak FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    streak = row[0] if row else 0

    # 1. ATS Apprentice (Analyzed >= 1 resume)
    cursor.execute("SELECT COUNT(*) FROM analyses WHERE user_id = ?", (user_id,))
    total_analyses = cursor.fetchone()[0]
    if total_analyses >= 1:
        unlocked.append("ATS Apprentice")

    # 2. ATS Master (Score >= 80)
    cursor.execute("SELECT COUNT(*) FROM analyses WHERE user_id = ? AND ats_score >= 80", (user_id,))
    high_score_count = cursor.fetchone()[0]
    if high_score_count >= 1:
        unlocked.append("ATS Master")

    # 3. Interview Ready (Did an Interview Prep activity)
    cursor.execute("SELECT COUNT(*) FROM user_activities WHERE user_id = ? AND activity_type = 'Interview Prep'", (user_id,))
    interview_activity = cursor.fetchone()[0]
    if interview_activity >= 1:
        unlocked.append("Interview Ready")

    # 4. Continuous Learner (Did a Learning Assistant guide)
    cursor.execute("SELECT COUNT(*) FROM user_activities WHERE user_id = ? AND activity_type = 'Learning Guide'", (user_id,))
    learning_activity = cursor.fetchone()[0]
    if learning_activity >= 1:
        unlocked.append("Continuous Learner")

    # 5. Web Artisan (Did a Portfolio compilation)
    cursor.execute("SELECT COUNT(*) FROM user_activities WHERE user_id = ? AND activity_type = 'Portfolio Builder'", (user_id,))
    portfolio_activity = cursor.fetchone()[0]
    if portfolio_activity >= 1:
        unlocked.append("Web Artisan")

    # 6. Streak Master (Streak >= 3)
    if streak >= 3:
        unlocked.append("Streak Master")

    conn.close()
    return unlocked


def process_xp_and_badges(user_id: int, xp_gain: int, activity_type: str) -> tuple:
    """
    Awards XP points to user and updates badges if any new badges are unlocked.
    Returns: (dict_of_updated_stats, newly_unlocked_badges_list)
    """
    # 1. Add XP and update streak in database
    stats = add_user_xp(user_id, xp_gain, activity_type)
    if not stats:
        return None, []

    # 2. Re-evaluate badges
    qualified_badges = evaluate_badges(user_id)
    
    # 3. Compare with currently saved badges
    user_info = get_user_by_id(user_id)
    current_badges = user_info.get("badges", [])
    
    newly_unlocked = []
    for badge in qualified_badges:
        if badge not in current_badges:
            newly_unlocked.append(badge)
            current_badges.append(badge)
            
    if newly_unlocked:
        # Update user's badges list in database
        update_user_badges(user_id, current_badges)
        
    return stats, newly_unlocked
