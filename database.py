"""
database.py - SQLite database operations for Resume Analyzer & Career Platform
Stores analyses, user credentials, gamification stats, job vacancy postings, and application pipelines.
"""

import sqlite3
import json
import hashlib
from datetime import datetime

DB_PATH = "resume_analyzer.db"


def hash_password(password: str) -> str:
    """Helper to hash passwords using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def init_db():
    """Initialize database and create tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Existing analyses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            resume_filename TEXT,
            job_title TEXT,
            company_name TEXT,
            ats_score INTEGER,
            match_score INTEGER,
            matched_skills TEXT,       -- JSON list
            missing_skills TEXT,       -- JSON list
            strengths TEXT,            -- JSON list
            improvements TEXT,         -- JSON list
            overall_summary TEXT,
            word_count INTEGER,
            user_id INTEGER           -- Link to users
        )
    """)

    # 2. Existing skill tracker table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skill_tracker (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill TEXT UNIQUE,
            times_required INTEGER DEFAULT 1,
            last_seen TEXT
        )
    """)

    # 3. Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,       -- 'student', 'recruiter', 'admin'
            xp INTEGER DEFAULT 0,
            streak INTEGER DEFAULT 0,
            last_activity TEXT,
            badges TEXT DEFAULT '[]'   -- JSON list of unlocked badges
        )
    """)

    # 4. User Activities table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            activity_type TEXT NOT NULL,
            xp_earned INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # 5. Jobs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            description TEXT NOT NULL,
            location TEXT,
            salary_range TEXT,
            required_skills TEXT       -- JSON list
        )
    """)

    # 6. Applications table (Job application pipeline tracking)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            job_title TEXT NOT NULL,
            company TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Applied', -- 'Applied', 'Screener', 'Technical', 'Behavioral', 'Offer', 'Rejected'
            date_applied TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()

    # Run migrations if columns are missing
    try:
        cursor.execute("ALTER TABLE analyses ADD COLUMN user_id INTEGER")
        conn.commit()
    except sqlite3.OperationalError:
        pass

    # Seed Default Users if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        default_users = [
            ("admin", hash_password("admin123"), "admin"),
            ("recruiter", hash_password("recruiter123"), "recruiter"),
            ("student", hash_password("student123"), "student")
        ]
        cursor.executemany("""
            INSERT INTO users (username, password_hash, role, xp, streak, last_activity, badges)
            VALUES (?, ?, ?, 0, 0, datetime('now'), '[]')
        """, default_users)
        conn.commit()

    # Seed Sample Jobs if empty
    cursor.execute("SELECT COUNT(*) FROM jobs")
    if cursor.fetchone()[0] == 0:
        sample_jobs = [
            ("Software Engineer", "Google", 
             "We are looking for a Software Engineer to develop next-generation technologies. Experience in Python, Go, Java, system design, data structures, and algorithms is required. Strong cloud services background (AWS/GCP) is a plus.", 
             "Mountain View, CA", "$150,000 - $190,000", 
             json.dumps(["Python", "Go", "Java", "System Design", "Data Structures", "Algorithms", "AWS", "GCP"])),
            
            ("Data Scientist", "Amazon", 
             "Join our AWS AI team. Responsibilities include building machine learning models using TensorFlow, PyTorch, and Scikit-learn. Proficiency in SQL, Python, Pandas, statistical testing, and cloud infrastructure required.", 
             "Seattle, WA", "$140,000 - $180,000", 
             json.dumps(["Python", "SQL", "Pandas", "TensorFlow", "PyTorch", "Scikit-learn", "Machine Learning"])),

            ("Product Manager", "Microsoft", 
             "Looking for an experienced Product Manager to lead cloud infrastructure initiatives. Requirements include technical product strategy, agile project management, SQL analysis, user experience optimization, and roadmapping.", 
             "Redmond, WA", "$130,000 - $175,000", 
             json.dumps(["Product Strategy", "Agile", "SQL", "User Experience", "Roadmapping", "Cloud"])),

            ("AI Engineer", "NVIDIA", 
             "Build the future of generative AI. Requires solid experience with deep learning, PyTorch, NVIDIA CUDA programming, large language models (LLMs), Python, and API deployment. Performance optimization experience required.", 
             "Santa Clara, CA", "$160,000 - $210,000", 
             json.dumps(["Python", "Deep Learning", "PyTorch", "CUDA", "LLMs", "Generative AI", "APIs"]))
        ]
        cursor.executemany("""
            INSERT INTO jobs (title, company, description, location, salary_range, required_skills)
            VALUES (?, ?, ?, ?, ?, ?)
        """, sample_jobs)
        conn.commit()

    conn.close()


def save_analysis(data: dict, user_id: int = None) -> int:
    """Save an analysis result to the database. Returns the new row ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO analyses (
            created_at, resume_filename, job_title, company_name,
            ats_score, match_score, matched_skills, missing_skills,
            strengths, improvements, overall_summary, word_count, user_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data.get("resume_filename", ""),
        data.get("job_title", ""),
        data.get("company_name", ""),
        data.get("ats_score", 0),
        data.get("match_score", 0),
        json.dumps(data.get("matched_skills", [])),
        json.dumps(data.get("missing_skills", [])),
        json.dumps(data.get("strengths", [])),
        json.dumps(data.get("improvements", [])),
        data.get("overall_summary", ""),
        data.get("word_count", 0),
        user_id
    ))

    new_id = cursor.lastrowid

    # Update skill tracker
    for skill in data.get("missing_skills", []):
        cursor.execute("""
            INSERT INTO skill_tracker (skill, times_required, last_seen)
            VALUES (?, 1, ?)
            ON CONFLICT(skill) DO UPDATE SET
                times_required = times_required + 1,
                last_seen = excluded.last_seen
        """, (skill, datetime.now().strftime("%Y-%m-%d")))

    conn.commit()
    conn.close()
    return new_id


def get_all_analyses(user_id: int = None) -> list:
    """Retrieve all past analyses, optionally filtered by user_id."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if user_id is not None:
        cursor.execute("SELECT * FROM analyses WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    else:
        cursor.execute("SELECT * FROM analyses ORDER BY created_at DESC")
        
    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        d = dict(row)
        d["matched_skills"] = json.loads(d["matched_skills"] or "[]")
        d["missing_skills"] = json.loads(d["missing_skills"] or "[]")
        d["strengths"] = json.loads(d["strengths"] or "[]")
        d["improvements"] = json.loads(d["improvements"] or "[]")
        results.append(d)
    return results


def get_top_missing_skills(limit: int = 10, user_id: int = None) -> list:
    """Get the most frequently missing skills."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if user_id is not None:
        cursor.execute("SELECT missing_skills FROM analyses WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        counts = {}
        for r in rows:
            skills = json.loads(r[0] or "[]")
            for s in skills:
                counts[s] = counts.get(s, 0) + 1
        sorted_skills = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:limit]
        conn.close()
        return [{"skill": k, "times_missing": v} for k, v in sorted_skills]
    else:
        cursor.execute("""
            SELECT skill, times_required FROM skill_tracker
            ORDER BY times_required DESC LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [{"skill": r[0], "times_missing": r[1]} for r in rows]


def get_score_trend(user_id: int = None) -> list:
    """Get ATS and match scores over time for trend chart."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if user_id is not None:
        cursor.execute("""
            SELECT created_at, ats_score, match_score, job_title
            FROM analyses WHERE user_id = ? ORDER BY created_at ASC
        """, (user_id,))
    else:
        cursor.execute("""
            SELECT created_at, ats_score, match_score, job_title
            FROM analyses ORDER BY created_at ASC
        """)
    rows = cursor.fetchall()
    conn.close()
    return [{"date": r[0], "ats": r[1], "match": r[2], "job": r[3]} for r in rows]


def delete_analysis(analysis_id: int):
    """Delete a specific analysis by ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM analyses WHERE id = ?", (analysis_id,))
    conn.commit()
    conn.close()


# ── NEW USER & AUTHENTICATION HELPER QUERIES ──

def get_user(username: str) -> dict:
    """Retrieve user details by username."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        d = dict(row)
        d["badges"] = json.loads(d["badges"] or "[]")
        return d
    return None


def get_user_by_id(user_id: int) -> dict:
    """Retrieve user details by user ID."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        d = dict(row)
        d["badges"] = json.loads(d["badges"] or "[]")
        return d
    return None


def create_user(username: str, password_hash: str, role: str) -> bool:
    """Create a new user. Returns True if successful, False if username taken."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (username, password_hash, role, xp, streak, last_activity, badges)
            VALUES (?, ?, ?, 0, 1, datetime('now'), '[]')
        """, (username, password_hash, role))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success


def get_all_users() -> list:
    """Get all registered users for Admin panel."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role, xp, streak, last_activity, badges FROM users ORDER BY xp DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def reset_user_xp(user_id: int):
    """Reset user XP and badges."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET xp = 0, badges = '[]', streak = 0 WHERE id = ?", (user_id,))
    cursor.execute("DELETE FROM user_activities WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


def update_user_role(user_id: int, new_role: str):
    """Change user role."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
    conn.commit()
    conn.close()


def delete_user(user_id: int):
    """Delete user and all their associated records."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    cursor.execute("DELETE FROM analyses WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM user_activities WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM applications WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


# ── NEW GAMIFICATION HELPER QUERIES ──

def add_user_xp(user_id: int, xp_gain: int, activity_type: str) -> dict:
    """Add XP to user profile, track activity, check streak, and return updated info."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get current user details
    cursor.execute("SELECT xp, streak, last_activity, badges FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
    
    current_xp, current_streak, last_activity, badges_json = row
    new_xp = current_xp + xp_gain

    # Check streak
    today_str = datetime.now().strftime("%Y-%m-%d")
    new_streak = current_streak
    if last_activity:
        last_active_date = last_activity.split(" ")[0]
        if last_active_date != today_str:
            # Check if active yesterday to increment, or reset
            try:
                delta = datetime.strptime(today_str, "%Y-%m-%d") - datetime.strptime(last_active_date, "%Y-%m-%d")
                if delta.days == 1:
                    new_streak += 1
                elif delta.days > 1:
                    new_streak = 1 # Reset to 1 day
            except Exception:
                new_streak = 1
    else:
        new_streak = 1

    # Save activity
    cursor.execute("""
        INSERT INTO user_activities (user_id, activity_type, xp_earned, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user_id, activity_type, xp_gain, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    # Update user record
    cursor.execute("""
        UPDATE users 
        SET xp = ?, streak = ?, last_activity = ?
        WHERE id = ?
    """, (new_xp, new_streak, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id))

    conn.commit()
    conn.close()

    return {"xp": new_xp, "streak": new_streak}


def update_user_badges(user_id: int, badges: list):
    """Save user badges list."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET badges = ? WHERE id = ?", (json.dumps(badges), user_id))
    conn.commit()
    conn.close()


def get_leaderboard(limit: int = 5) -> list:
    """Retrieve top users based on XP."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username, xp, streak, role FROM users 
        WHERE role = 'student' 
        ORDER BY xp DESC LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [{"username": r[0], "xp": r[1], "streak": r[2], "role": r[3]} for r in rows]


# ── JOBS MANAGEMENT QUERIES ──

def get_all_jobs() -> list:
    """Retrieve all jobs in database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for row in rows:
        d = dict(row)
        d["required_skills"] = json.loads(d["required_skills"] or "[]")
        results.append(d)
    return results


def save_job(title: str, company: str, description: str, location: str, salary_range: str, required_skills: list):
    """Add a new job vacancy."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO jobs (title, company, description, location, salary_range, required_skills)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, company, description, location, salary_range, json.dumps(required_skills)))
    conn.commit()
    conn.close()


def delete_job(job_id: int):
    """Delete a job by ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()


# ── APPLICATIONS PIPELINE QUERIES ──

def get_user_applications(user_id: int) -> list:
    """Get all job applications tracked by a user."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applications WHERE user_id = ? ORDER BY date_applied DESC", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_user_application(user_id: int, job_title: str, company: str, status: str = 'Applied') -> int:
    """Add a tracked application record."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO applications (user_id, job_title, company, status, date_applied)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, job_title, company, status, datetime.now().strftime("%Y-%m-%d")))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id


def update_application_status(app_id: int, new_status: str):
    """Update status of a specific job application."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE applications SET status = ? WHERE id = ?", (new_status, app_id))
    conn.commit()
    conn.close()


def delete_application(app_id: int):
    """Remove a job application record from tracker."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applications WHERE id = ?", (app_id,))
    conn.commit()
    conn.close()


# ── ADMIN STATISTICS QUERY ──

def get_system_stats() -> dict:
    """Retrieve quick system metrics for Admin Dashboard."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Total users
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    # 2. Total analyses
    cursor.execute("SELECT COUNT(*) FROM analyses")
    total_analyses = cursor.fetchone()[0]

    # 3. Total jobs
    cursor.execute("SELECT COUNT(*) FROM jobs")
    total_jobs = cursor.fetchone()[0]

    # 4. Roles split
    cursor.execute("SELECT role, COUNT(*) FROM users GROUP BY role")
    roles_split = dict(cursor.fetchall())

    # 5. Average ATS score
    cursor.execute("SELECT AVG(ats_score) FROM analyses")
    avg_score = cursor.fetchone()[0] or 0.0

    conn.close()
    return {
        "total_users": total_users,
        "total_analyses": total_analyses,
        "total_jobs": total_jobs,
        "roles": roles_split,
        "avg_ats_score": round(avg_score, 1)
    }