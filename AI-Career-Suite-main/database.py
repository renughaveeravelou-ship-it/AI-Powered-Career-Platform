"""
database.py - SQLite database operations for Resume Analyzer
Stores all analysis history so users can track their progress over time.
"""

import sqlite3
import json
from datetime import datetime

DB_PATH = "resume_analyzer.db"


def init_db():
    """Initialize database and create tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

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
            word_count INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skill_tracker (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill TEXT UNIQUE,
            times_required INTEGER DEFAULT 1,
            last_seen TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_analysis(data: dict) -> int:
    """Save an analysis result to the database. Returns the new row ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO analyses (
            created_at, resume_filename, job_title, company_name,
            ats_score, match_score, matched_skills, missing_skills,
            strengths, improvements, overall_summary, word_count
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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


def get_all_analyses() -> list:
    """Retrieve all past analyses, newest first."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

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


def get_top_missing_skills(limit: int = 10) -> list:
    """Get the most frequently missing skills across all analyses."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT skill, times_required FROM skill_tracker
        ORDER BY times_required DESC LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [{"skill": r[0], "times_missing": r[1]} for r in rows]


def get_score_trend() -> list:
    """Get ATS and match scores over time for trend chart."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
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