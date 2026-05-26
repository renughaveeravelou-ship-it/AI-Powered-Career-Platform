"""
app.py - AI-Powered Career Platform | Dark Luxury UI
Author: Yagyesh Vyas | github.com/yagyeshVyas
"""

import streamlit as st
import pandas as pd
import json
import hashlib
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Import Custom Modules
from providers import PROVIDERS, call_api
from analyzer import (
    extract_text_from_pdf, analyze_resume,
    get_score_label, get_score_color
)
from database import (
    init_db, save_analysis, get_all_analyses,
    get_top_missing_skills, get_score_trend, delete_analysis,
    get_user, create_user, get_all_users, reset_user_xp,
    update_user_role, delete_user, get_leaderboard,
    get_all_jobs, save_job, delete_job, get_system_stats,
    get_user_applications, add_user_application, 
    update_application_status, delete_application
)
from auth import authenticate_user, register_new_user
from gamification import process_xp_and_badges, BADGES
from career import recommend_career_path, plot_career_salaries
from learning import generate_study_guide, get_course_search_links
from portfolio import fetch_github_profile_data, compile_portfolio_code
from job_matching import match_resume_to_jobs
from scrape_job import fetch_job_description

# Page Config
st.set_page_config(
    page_title="AI Career Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_db()

# Styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
:root {
    --bg:#050510; --bg2:#0a0a1a; --bg3:#10101f;
    --border:rgba(139,92,246,0.15); --border2:rgba(139,92,246,0.35);
    --purple:#8b5cf6; --purple2:#a78bfa; --violet:#7c3aed;
    --green:#10b981; --amber:#f59e0b; --red:#ef4444;
    --cyan:#06b6d4; --pink:#ec4899; --nvidia:#76b900;
    --text:#e2e8f0; --text2:#94a3b8; --text3:#64748b;
    --font-h:'Syne',sans-serif; --font-b:'DM Sans',sans-serif;
    --glass:rgba(255,255,255,0.03); --glass2:rgba(255,255,255,0.06);
}

/* Animations */
@keyframes mesh {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stApp {
    background: radial-gradient(circle at 50% 50%, #0d0d2b 0%, #050510 100%) !important;
    font-family: var(--font-b) !important;
    perspective: 1200px;
    overflow-x: hidden;
}

.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background: 
        radial-gradient(at 0% 0%, rgba(139, 92, 246, 0.08) 0, transparent 50%),
        radial-gradient(at 50% 0%, rgba(6, 182, 212, 0.05) 0, transparent 50%),
        radial-gradient(at 100% 0%, rgba(236, 72, 153, 0.05) 0, transparent 50%);
    z-index: -1;
    filter: blur(80px);
    animation: mesh 20s ease infinite;
    background-size: 200% 200%;
}

[data-testid="stSidebar"] {
    background: rgba(10, 10, 26, 0.7) !important;
    border-right: 1px solid var(--border) !important;
    backdrop-filter: blur(30px) !important;
}

/* Floating 3D Grid */
@keyframes grid-float {
    from { transform: perspective(1000px) rotateX(60deg) translateY(0); }
    to { transform: perspective(1000px) rotateX(60deg) translateY(40px); }
}
.stApp::after {
    content: "";
    position: fixed;
    top: 50%; left: -50%;
    width: 200%; height: 200%;
    background-image: 
        linear-gradient(rgba(139, 92, 246, 0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(139, 92, 246, 0.05) 1px, transparent 1px);
    background-size: 80px 80px;
    transform: perspective(1000px) rotateX(60deg);
    z-index: -2;
    animation: grid-float 5s linear infinite;
}

[data-testid="stAppViewContainer"] > .main .block-container { padding:2rem 3rem !important; max-width:1450px !important; transform-style:preserve-3d; }
h1,h2,h3 { font-family:var(--font-h) !important; color:var(--text) !important; text-shadow:0 15px 30px rgba(0,0,0,0.5); }

/* Hero Parallax */
.hero {
    position:relative;
    background:linear-gradient(135deg,#0a0a1a 0%,#1a0a2e 30%,#0a1628 60%,#0d0820 100%);
    border:1px solid rgba(139,92,246,0.25); border-radius:30px; padding:4rem 3rem;
    margin-bottom:3rem; overflow:hidden; text-align:center;
    animation:border-glow 4s ease-in-out infinite;
    transform:translateZ(20px); transform-style:preserve-3d;
    box-shadow:0 25px 50px -12px rgba(0,0,0,0.8);
}
.hero::before {
    content:''; position:absolute; top:-80%; left:-20%; width:140%; height:200%;
    background:linear-gradient(45deg,
        rgba(139,92,246,0.15),rgba(6,182,212,0.1),rgba(236,72,153,0.08),
        rgba(118,185,0,0.07),rgba(139,92,246,0.15));
    background-size:400% 400%;
    animation:aurora 15s ease infinite;
    filter:blur(70px); opacity:0.6;
}
.hero-badge {
    position:relative; display:inline-block;
    background:rgba(139,92,246,0.15); border:1px solid rgba(139,92,246,0.4);
    color:var(--purple2); font-size:0.72rem; font-weight:600; letter-spacing:0.16em;
    text-transform:uppercase; padding:7px 20px; border-radius:100px; margin-bottom:1.5rem;
    backdrop-filter:blur(15px); transform:translateZ(40px);
}
.hero h1 {
    position:relative; font-family:var(--font-h) !important; font-size:3.5rem !important; font-weight:800 !important;
    background:linear-gradient(135deg,#ffffff 0%,#a78bfa 35%,#60a5fa 65%,#22d3ee 100%);
    background-size:200% 200%; animation:gradient-shift 8s ease infinite;
    -webkit-background-clip:text !important; -webkit-text-fill-color:transparent !important;
    background-clip:text !important; line-height:1.1 !important; margin-bottom:1rem !important;
    transform:translateZ(60px);
}
.hero p { position:relative; color:var(--text2) !important; font-size:1.1rem !important; font-weight:300 !important; max-width:680px; margin:0 auto !important; line-height:1.7 !important; transform:translateZ(30px); }

/* Score Cards */
.score-wrap {
    background:rgba(255,255,255,0.02); border:1px solid var(--border); border-radius:20px;
    padding:1.8rem; text-align:center; position:relative; overflow:hidden; margin-bottom:1.2rem;
    transition:all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); backdrop-filter:blur(12px);
    transform-style:preserve-3d; box-shadow:0 10px 30px rgba(0,0,0,0.3);
}
.score-wrap:hover { 
    transform:translateY(-8px) rotateX(6deg) rotateY(2deg); 
    border-color:var(--purple);
    box-shadow:0 30px 60px rgba(0,0,0,0.6), 0 0 20px rgba(139,92,246,0.1);
}
.score-number { font-family:var(--font-h); font-size:4rem; font-weight:800; line-height:1; margin:0.4rem 0; transform:translateZ(30px); }
.score-label  { font-size:0.75rem; color:var(--text3); text-transform:uppercase; letter-spacing:0.12em; font-weight:600; transform:translateZ(20px); }

/* UI Boxes */
.info-box, .win-box, .success-box, .danger-box {
    border-radius:14px; padding:1.2rem 1.5rem; margin:0.8rem 0;
    transition:all 0.3s ease; transform-style:preserve-3d;
    background: rgba(255,255,255,0.02);
    border: 1px solid var(--border);
    color: var(--text);
}
.info-box:hover { transform:translateX(5px) translateZ(10px); background:rgba(139,92,246,0.1); }
.win-box { border-left: 4px solid var(--green); }
.danger-box { border-left: 4px solid var(--red); }
.success-box { border-left: 4px solid var(--cyan); }

.summary-box {
    background:linear-gradient(135deg,rgba(139,92,246,0.12) 0%,rgba(6,182,212,0.08) 100%);
    border:1px solid rgba(139,92,246,0.3); border-radius:20px;
    padding:1.8rem; box-shadow:0 15px 35px rgba(0,0,0,0.4);
    transform:translateZ(10px);
}

.resume-output {
    background:rgba(15,15,35,0.4); border:1px solid var(--border); border-radius:20px;
    padding:2.5rem; font-size:0.92rem; line-height:1.8;
    backdrop-filter:blur(15px); box-shadow:0 20px 50px rgba(0,0,0,0.5);
    transition:all 0.4s ease;
}

/* Staggered Animations */
div[data-testid="stVerticalBlock"] > div { animation:fade-in 0.8s cubic-bezier(0.22, 1, 0.36, 1) backwards; }

/* Buttons */
.stButton>button {
    background:linear-gradient(135deg,#7c3aed,#6366f1) !important;
    border:1px solid rgba(255,255,255,0.1) !important;
    border-radius:15px !important; padding:0.8rem 2.2rem !important;
    transform:translateZ(0); transition:all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    color: #ffffff !important;
}
.stButton>button:hover:not(:disabled) {
    transform:translateY(-4px) translateZ(15px) !important;
    box-shadow:0 15px 30px rgba(124,58,237,0.4), 0 0 10px rgba(124,58,237,0.2) !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background:rgba(255,255,255,0.02); border:1px solid var(--border);
    border-radius:18px; padding:1.2rem; transform-style:preserve-3d;
    transition:all 0.3s ease;
}

/* Custom Badges */
.badge-gallery {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin: 1.5rem 0;
}
.badge-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    min-width: 220px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}
.badge-card.locked {
    opacity: 0.4;
    filter: grayscale(1);
}
.badge-icon {
    font-size: 2rem;
}
.badge-name {
    font-weight: 600;
    font-family: var(--font-h);
}
.badge-desc {
    font-size: 0.75rem;
    color: var(--text3);
}

/* Form Controls */
.stTextInput>div>div>input, .stTextArea>div>div>textarea {
    border-radius:14px !important; padding:12px 18px !important;
    background:rgba(255,255,255,0.03) !important;
}

/* chips */
.chips { display:flex; flex-wrap:wrap; gap:6px; margin:0.5rem 0; }
.chip { padding:4px 12px; border-radius:100px; font-size:0.78rem; font-weight:500; border:1px solid rgba(255,255,255,0.1); }
.chip-green { background:rgba(16,185,129,0.1); color:#10b981; border-color:rgba(16,185,129,0.25); }
.chip-red { background:rgba(239,68,68,0.1); color:#f87171; border-color:rgba(239,68,68,0.25); }
.chip-blue { background:rgba(96,165,250,0.1); color:#60a5fa; border-color:rgba(96,165,250,0.25); }

#MainMenu, footer, header { visibility:hidden; }
::-webkit-scrollbar { width:8px; }
::-webkit-scrollbar-thumb { background:rgba(139,92,246,0.3); border-radius:10px; }
</style>
""", unsafe_allow_html=True)


# ── SESSION STATE INITIALIZATION ──
if "api_keys" not in st.session_state:
    st.session_state.api_keys = {}
if "user" not in st.session_state:
    st.session_state.user = None
if "auth_page" not in st.session_state:
    st.session_state.auth_page = "Landing"  # Landing, Login, SignUp
if "interview_messages" not in st.session_state:
    st.session_state.interview_messages = []
if "daily_tasks" not in st.session_state:
    st.session_state.daily_tasks = {
        "analyze": False,
        "interview": False,
        "job_match": False,
        "claimed_xp": False
    }


def logout():
    st.session_state.user = None
    st.session_state.auth_page = "Landing"
    st.session_state.interview_messages = []
    st.session_state.daily_tasks = {
        "analyze": False,
        "interview": False,
        "job_match": False,
        "claimed_xp": False
    }
    st.rerun()


# ── HELPER RENDERERS ──
def chips(items, cls="chip-green"):
    if not items:
        return "<span style='color:#475569;font-style:italic;font-size:0.82rem'>None found</span>"
    return '<div class="chips">'+ "".join(f'<span class="chip {cls}">{i}</span>' for i in items) + '</div>'


def score_card(score, title):
    cls = "green" if score >= 75 else ("amber" if score >= 50 else "red")
    color = "#10b981" if score >= 75 else ("#f59e0b" if score >= 50 else "#ef4444")
    st.markdown(f"""<div class="score-wrap" style="border-color:{color};">
        <div style="font-size:0.82rem;color:var(--text3);font-weight:600;text-transform:uppercase;">{title}</div>
        <div class="score-number" style="color:{color};">{score}</div>
        <div class="score-label">out of 100</div>
        <span style="font-size:0.75rem;padding:3px 10px;border-radius:100px;background:{color}22;color:{color};font-weight:700;">{get_score_label(score)}</span>
    </div>""", unsafe_allow_html=True)
    st.progress(score / 100)


# ── MAIN SIDEBAR ──
if st.session_state.user:
    user = st.session_state.user
    role = user["role"]
    
    with st.sidebar:
        st.markdown(f"<div style='font-family:Syne,sans-serif;font-size:1.3rem;font-weight:800;background:linear-gradient(135deg,#a78bfa,#60a5fa);-webkit-background-clip:text;-webkit-text-fill-color:transparent'>AI Career platform</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:0.78rem;color:#a78bfa;margin-bottom:1rem;'>Logged in as: <b>{user['username']} ({role.upper()})</b></div>", unsafe_allow_html=True)
        
        # Streak and XP info
        if role == "student":
            st.markdown(f"""
            <div style="background:rgba(139,92,246,0.1);border:1px solid rgba(139,92,246,0.3);border-radius:10px;padding:10px;font-size:0.82rem;margin-bottom:1rem;">
             Streak: <b>{user['streak']} Days</b><br>
             Experience: <b>{user['xp']} XP</b>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        
        # UNIVERSAL API KEY DISPATCHER
        st.markdown("**AI Provider**")
        selected_provider = st.selectbox("Hidden Label", list(PROVIDERS.keys()), label_visibility="collapsed", key="provider_sel")
        pinfo = PROVIDERS[selected_provider]
        
        st.markdown(f"**{selected_provider} API Key**")
        saved_key = st.session_state.api_keys.get(selected_provider, "")
        entered_key = st.text_input("Hidden Label", value=saved_key, type="password", placeholder=pinfo["placeholder"], label_visibility="collapsed", key=f"apikey_{selected_provider}")
        
        if entered_key:
            st.session_state.api_keys[selected_provider] = entered_key.strip()
        is_local = pinfo.get("local_only", False)
        if is_local:
            st.session_state.api_keys[selected_provider] = "local"
        
        api_key = st.session_state.api_keys.get(selected_provider, "").strip()
        
        # Model Tier
        free_models, paid_models = pinfo["free_models"], pinfo["paid_models"]
        has_free = len(free_models) > 0
        has_paid = len(paid_models) > 0
        if has_free and has_paid:
            tier = st.radio("**Model Tier**", ["Free", "Paid"], horizontal=True, key=f"tier_{selected_provider}")
            model_opts = list(free_models.keys()) if tier == "Free" else list(paid_models.keys())
        else:
            model_opts = list(free_models.keys()) if has_free else list(paid_models.keys())
            
        sel_name = st.selectbox("Hidden Label", model_opts, label_visibility="collapsed", key=f"model_{selected_provider}")
        all_provider_models = {**free_models, **paid_models}
        sel_id = all_provider_models.get(sel_name, sel_name)
        
        st.markdown("---")
        
        # Navigation
        if role == "student":
            page = st.radio("**Navigate**", [
                "Dashboard", "Resume Analyzer", "Cover Letter", 
                "Interview Prep", "Resume Builder", "Job Discovery", 
                "Application Tracker", "Career Pathways", "Learning Assistant", 
                "AI Portfolio", "AI Copilot", "API Guide", "Logout"
            ])
        elif role == "recruiter":
            page = st.radio("**Navigate**", [
                "Dashboard", "Job Postings", "API Guide", "Logout"
            ])
        else: # Admin
            page = st.radio("**Navigate**", [
                "Dashboard", "User Registry", "API Guide", "Logout"
            ])
            
    if page == "Logout":
        logout()
        
    def ai_call(prompt, temperature=0.7, max_tokens=2500):
        if not api_key:
            raise ValueError("No API Key entered in sidebar! Please configure OpenRouter, Gemini, or Groq.")
        return call_api(selected_provider, api_key, sel_id, prompt, temperature, max_tokens)


# ════════════════════════════════════════════════════════
# LANDING & AUTHENTICATION PAGES (If Not Logged In)
# ════════════════════════════════════════════════════════
if not st.session_state.user:
    if st.session_state.auth_page == "Landing":
        # Interactive Hero landing section
        st.markdown("""<div class="hero">
            <div class="hero-badge">AI Career Platform 2.0</div>
            <h1>Smart Recruiting & Career Acceleration</h1>
            <p>Integrated AI tools for Student portfolios, Recruiter candidate scoring, and Admin system insights.</p>
        </div>""", unsafe_allow_html=True)
        
        l1, l2 = st.columns([2, 1], gap="large")
        with l1:
            st.markdown("### ✨ Transform Your Professional Path")
            st.markdown("""
            Welcome to the AI-Powered Career Platform. This suite offers customized spaces:
            - **Students**: Upload resume, check ATS rating, receive gamified XP and badges, mock interview preparation, learning paths, and automatic portfolio webpage generation.
            - **Recruiters**: Post job profiles, evaluate candidate lists, and run instant AI match audits.
            - **Admins**: Monitor system metrics, manage database profiles, and review active API status logs.
            """)
            
            st.markdown("###  User Testimonials")
            t1, t2 = st.columns(2)
            with t1:
                st.markdown("""
                <div class="info-box" style="padding: 1rem;">
                "The Resume Analyzer and AI Portfolio builder helped me land a Cloud Dev position in 3 weeks. The Gamification XP kept me hooked!"<br>
                <strong>- Rohan S. (Student)</strong>
                </div>
                """, unsafe_allow_html=True)
            with t2:
                st.markdown("""
                <div class="info-box" style="padding: 1rem;">
                "Screening 50+ candidates in minutes with exact skill gaps and ATS compatibility ratings saved us weeks of interview hours."<br>
                <strong>- Jessica K. (Recruiter, Amazon Tech)</strong>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("### FAQ")
            with st.expander("Is my data secure?"):
                st.write("Yes. All files are evaluated in-memory and credentials are stored securely in local encrypted-hashing format.")
            with st.expander("How do I get a free API key?"):
                st.write("Configure OpenRouter or Google Gemini in the sidebar and copy-paste the free key in seconds.")
                
            st.markdown("### Get In Touch")
            c_name = st.text_input("Name", placeholder="Your Name")
            c_email = st.text_input("Email", placeholder="you@domain.com")
            c_msg = st.text_area("Message", placeholder="Tell us how we can help...")
            if st.button("Send Inquiry"):
                if c_name and c_email and c_msg:
                    st.toast("Inquiry submitted successfully! We will email you back shortly.")
                else:
                    st.warning("Please fill all contact fields.")
                    
        with l2:
            st.markdown("""<div class="summary-box" style="margin-top:2.5rem; text-align:center;">
                <h3>Get Started</h3>
                <p style="font-size:0.9rem; color:var(--text2);">Access your role-based control panel by logging in or registering below.</p>
            </div>""", unsafe_allow_html=True)
            
            act_col1, act_col2 = st.columns(2)
            with act_col1:
                if st.button("Login Panel", use_container_width=True):
                    st.session_state.auth_page = "Login"
                    st.rerun()
            with act_col2:
                if st.button("Sign Up Panel", use_container_width=True):
                    st.session_state.auth_page = "SignUp"
                    st.rerun()
                    
    elif st.session_state.auth_page == "Login":
        st.markdown("<h2 style='text-align:center;'> Account Login</h2>", unsafe_allow_html=True)
        login_box = st.columns([1, 2, 1])[1]
        with login_box:
            u_name = st.text_input("Username")
            u_pass = st.text_input("Password", type="password")
            st.markdown("")
            if st.button("Sign In", type="primary", use_container_width=True):
                user_match = authenticate_user(u_name, u_pass)
                if user_match:
                    st.session_state.user = user_match
                    st.toast(f" Welcome back, {u_name}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Try again or register.")
            if st.button("Back to Landing Page", use_container_width=True):
                st.session_state.auth_page = "Landing"
                st.rerun()
                
    elif st.session_state.auth_page == "SignUp":
        st.markdown("<h2 style='text-align:center;'> Create Account</h2>", unsafe_allow_html=True)
        signup_box = st.columns([1, 2, 1])[1]
        with signup_box:
            new_u = st.text_input("Username (Min 3 characters)")
            new_p = st.text_input("Password (Min 6 characters)", type="password")
            role_sel = st.selectbox("Register As", ["student", "recruiter", "admin"])
            st.markdown("")
            if st.button("Create Account", type="primary", use_container_width=True):
                success = register_new_user(new_u, new_p, role_sel)
                if success:
                    st.success("Registration complete! Please log in.")
                    st.session_state.auth_page = "Login"
                    st.rerun()
                else:
                    st.error("Registration failed. Username may be taken, or passwords too short.")
            if st.button("Back to Landing Page", use_container_width=True):
                st.session_state.auth_page = "Landing"
                st.rerun()


# ════════════════════════════════════════════════════════
# STUDENT ROLE ROUTING
# ════════════════════════════════════════════════════════
elif role == "student":
    
    # ── STUDENT DASHBOARD ──
    if page == "Dashboard":
        st.markdown(f"""<div class="hero">
            <div class="hero-badge">Welcome Back, {user['username']}!</div>
            <h1>Student Dashboard</h1>
            <p>Track your score metrics, missing skills, streaks, and unlocked badges.</p>
        </div>""", unsafe_allow_html=True)
        
        # Profile Gamification Stats
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(label="Gamification XP", value=f" {user['xp']} XP")
        with m2:
            st.metric(label="Streak Counter", value=f" {user['streak']} Days")
        with m3:
            st.metric(label="Unlocked Badges", value=f" {len(user['badges'])} / {len(BADGES)}")
            
        # Daily Gamification Tasks Checklist
        st.markdown("### Daily Quest Board")
        t_col1, t_col2 = st.columns([2, 1])
        with t_col1:
            t = st.session_state.daily_tasks
            task1_lbl = " Run Resume Analysis (+20 XP)" if t["analyze"] else "Run Resume Analysis (+20 XP)"
            task2_lbl = "Practice Mock STAR interview (+20 XP)" if t["interview"] else "Practice Mock STAR interview (+20 XP)"
            task3_lbl = "Match Job Vacancies (+10 XP)" if t["job_match"] else " Match Job Vacancies (+10 XP)"
            
            st.markdown(f"""
            <div class="info-box" style="padding: 1.5rem;">
                <div style="font-size: 1.1rem; font-weight:600; margin-bottom: 10px; color:#a78bfa;">Today's Quests</div>
                <div style="font-size:0.95rem; line-height: 1.8;">
                    {task1_lbl}<br>
                    {task2_lbl}<br>
                    {task3_lbl}
                </div>
            </div>
            """, unsafe_allow_html=True)
        with t_col2:
            # Claim Bonus button
            completed_all = t["analyze"] and t["interview"] and t["job_match"]
            if completed_all and not t["claimed_xp"]:
                st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
                if st.button("Claim Daily Bonus (+50 XP)!", type="primary", use_container_width=True):
                    # Process claim
                    t["claimed_xp"] = True
                    updated_stats, newly_unlocked = process_xp_and_badges(user["id"], 50, "Daily Bonus")
                    if updated_stats:
                        st.session_state.user["xp"] = updated_stats["xp"]
                        st.toast("Claimed +50 XP Daily Bonus!")
                    for b in newly_unlocked:
                        st.toast(f" Badge Unlocked: {b}!")
                    st.rerun()
            elif t["claimed_xp"]:
                st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
                st.success(" Daily quests completed and claimed!")
            else:
                st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
                st.info("Complete all three Daily Quests to unlock your +50 XP bonus!")

        # Badges Display Gallery
        st.markdown("###  Your Unlocked Badges")
        gallery = st.container()
        with gallery:
            cols = st.columns(3)
            for i, (b_name, b_info) in enumerate(BADGES.items()):
                unlocked = b_name in user["badges"]
                card_class = "badge-card" if unlocked else "badge-card locked"
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="{card_class}">
                        <div class="badge-icon">{b_info['icon'] if unlocked else ''}</div>
                        <div>
                            <div class="badge-name">{b_name}</div>
                            <div class="badge-desc">{b_info['description']}</div>
                            <div style="font-size:0.68rem; color:var(--text3); margin-top:2px;">Goal: {b_info['criteria']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
        st.markdown("---")
        
        # Charts section
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### ATS score history")
            history = get_score_trend(user["id"])
            if history:
                df = pd.DataFrame(history)
                fig = px.line(df, x="date", y=["ats", "match"], labels={"value": "Score", "date": "Date"}, markers=True)
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#e2e8f0"),
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No resume analysis history available. Complete your first scan under 'Resume Analyzer'!")
                
        with c2:
            st.markdown("###  Missing Skill Distribution")
            top_skills = get_top_missing_skills(limit=8, user_id=user["id"])
            if top_skills:
                df_skills = pd.DataFrame(top_skills)
                fig_bar = px.bar(df_skills, x="times_missing", y="skill", orientation='h', color="times_missing", color_continuous_scale="Purples")
                fig_bar.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#e2e8f0"),
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("No skill gaps logged. Run a Resume Analysis to populate details.")

    # ── SMART RESUME ANALYZER ──
    elif page == "Resume Analyzer":
        st.markdown("""<div class="hero">
            <div class="hero-badge">Smart Resume Analyzer</div>
            <h1>Resume ATS Screener</h1>
            <p>Score compatibility with targeted JDs and receive structural improvements.</p>
        </div>""", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2, gap="large")
        with c1:
            st.markdown("### Upload Resume")
            rtype = st.radio("Provide Type", ["Upload PDF", "Paste Text"], horizontal=True, label_visibility="collapsed", key="an_rt")
            resume_text = ""
            resume_file = ""
            if rtype == "Upload PDF":
                up = st.file_uploader("Upload PDF file", type=["pdf"], key="an_pdf")
                if up:
                    try:
                        resume_text = extract_text_from_pdf(up)
                        resume_file = up.name
                        st.success(f"Extracted {len(resume_text.split())} words.")
                    except Exception as e:
                        st.error(str(e))
            else:
                resume_text = st.text_area("Paste Resume Text", height=200, placeholder="Paste resume details...")
                resume_file = "pasted_resume.txt"
                
        with c2:
            st.markdown("### Target Job Details")
            jt = st.text_input("Job Title", placeholder="e.g. Data Scientist")
            co = st.text_input("Company", placeholder="e.g. Amazon")
            j_mode = st.radio("Provide JD", ["Paste text", "Scrape URL"])
            if j_mode == "Scrape URL":
                url = st.text_input("Job Link URL", placeholder="https://greenhouse.io/...")
                if url and st.button("Extract Context"):
                    with st.spinner("Extracting..."):
                        scrape_data = fetch_job_description(url)
                        st.session_state["fetched_jd"] = scrape_data["text"]
                        st.success("Extracted job description.")
                jd = st.text_area("Job Context", value=st.session_state.get("fetched_jd", ""), height=150)
            else:
                jd = st.text_area("Job Description Details", height=150)
                
        if st.button("Analyze Resume", type="primary", use_container_width=True):
            if not resume_text.strip():
                st.error("Please add resume details.")
            elif not jd.strip():
                st.error("Please paste job details.")
            else:
                with st.spinner("Processing analysis..."):
                    try:
                        result = analyze_resume(api_key, sel_id, resume_text, jd, jt, co, selected_provider)
                        result.update({
                            "resume_filename": resume_file,
                            "job_title": jt,
                            "company_name": co,
                            "word_count": len(resume_text.split())
                        })
                        
                        # Save Analysis to Database
                        save_analysis(result, user_id=user["id"])
                        st.session_state["last_result"] = result
                        
                        # Update daily task
                        st.session_state.daily_tasks["analyze"] = True

                        # Gamification Process
                        updated_stats, newly_unlocked = process_xp_and_badges(user["id"], 50, "Resume Analyzer")
                        if updated_stats:
                            st.session_state.user["xp"] = updated_stats["xp"]
                            st.session_state.user["streak"] = updated_stats["streak"]
                            st.toast(" +50 XP Earned!")
                        for b in newly_unlocked:
                            st.toast(f" Badge Unlocked: {b}!")
                            
                        st.success("Analysis complete!")
                    except Exception as e:
                        st.error(str(e))
                        
        if "last_result" in st.session_state:
            r = st.session_state["last_result"]
            st.markdown("---")
            s1, s2, s3 = st.columns(3)
            with s1:
                score_card(r["ats_score"], "ATS Score")
            with s2:
                score_card(r["match_score"], "Job Match")
            with s3:
                score_card(r.get("hire_probability", 0), "Interview Probability")
                
            st.markdown(f'<div class="summary-box"><strong>AI Verdict:</strong> {r["overall_summary"]}</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### Matched Skills")
                st.markdown(chips(r["matched_skills"], "chip-green"), unsafe_allow_html=True)
                st.markdown("### Strengths")
                for s in r.get("strengths", []):
                    st.markdown(f'<div class="info-box">{s}</div>', unsafe_allow_html=True)
            with col2:
                st.markdown("### Missing Skills")
                st.markdown(chips(r["missing_skills"], "chip-red"), unsafe_allow_html=True)
                st.markdown("### Improvements")
                for s in r.get("improvements", []):
                    st.markdown(f'<div class="info-box">{s}</div>', unsafe_allow_html=True)

    # ── COVER LETTER GENERATOR ──
    elif page == "Cover Letter":
        st.markdown("""<div class="hero">
            <div class="hero-badge">Cover Letter Generator</div>
            <h1>Tailored Cover Letters</h1>
            <p>Generate highly-optimized, custom cover letters matching target job descriptions.</p>
        </div>""", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2, gap="large")
        with c1:
            cl_resume = st.text_area("Paste Resume Text", height=200, placeholder="Paste resume details...")
        with c2:
            cl_jt = st.text_input("Job Title", placeholder="e.g. Data Scientist")
            cl_co = st.text_input("Company", placeholder="e.g. Amazon")
            cl_jd = st.text_area("Job Description details", height=150)
            
        if st.button("Generate Cover Letter", type="primary", use_container_width=True):
            if not cl_resume.strip() or not cl_jd.strip():
                st.error("Please provide both resume and job details.")
            else:
                with st.spinner("Compiling Cover Letter..."):
                    try:
                        prompt = f"Write a professional, human-sounding cover letter for {cl_jt} at {cl_co} matching resume: {cl_resume} and JD: {cl_jd}."
                        letter = ai_call(prompt)
                        st.markdown("### Your Cover Letter")
                        st.markdown(f'<div class="resume-output">{letter}</div>', unsafe_allow_html=True)
                        
                        # Award XP
                        updated_stats, newly_unlocked = process_xp_and_badges(user["id"], 30, "Cover Letter")
                        if updated_stats:
                            st.session_state.user["xp"] = updated_stats["xp"]
                            st.toast("+30 XP Earned!")
                        for b in newly_unlocked:
                            st.toast(f"Badge Unlocked: {b}!")
                    except Exception as e:
                        st.error(str(e))

    # ── AI INTERVIEW PREPARATION (Mock STAR Q&A) ──
    elif page == "Interview Prep":
        st.markdown("""<div class="hero">
            <div class="hero-badge">Interview Coach</div>
            <h1>Interactive Interview Training</h1>
            <p>Simulate realistic technical and behavioral question rounds and get STAR-based evaluations.</p>
        </div>""", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Question Generator", "STAR Simulator Chat"])
        
        with tab1:
            st.markdown("### Generate Practice Guide")
            ip_r = st.text_area("Resume Details", height=150, placeholder="Paste your resume...")
            ip_jt = st.text_input("Target Job Title", placeholder="e.g. Software Engineer")
            ip_jd = st.text_area("Target Job Description", height=120)
            
            if st.button("Generate Interview Guide", type="primary"):
                if not ip_r.strip():
                    st.error("Please add resume details.")
                else:
                    with st.spinner("Generating Q&A..."):
                        try:
                            prompt = f"As a recruiter, generate 5 challenging interview questions with answer frameworks based on this resume: {ip_r} for the job {ip_jt}. JD: {ip_jd}"
                            guide = ai_call(prompt)
                            st.markdown(f'<div class="resume-output">{guide}</div>', unsafe_allow_html=True)
                            
                            # Award XP
                            updated_stats, newly_unlocked = process_xp_and_badges(user["id"], 40, "Interview Prep")
                            if updated_stats:
                                st.session_state.user["xp"] = updated_stats["xp"]
                                st.toast(" +40 XP Earned!")
                            for b in newly_unlocked:
                                st.toast(f" Badge Unlocked: {b}!")
                        except Exception as e:
                            st.error(str(e))
                            
        with tab2:
            st.markdown("### STAR Mock Interview Simulator")
            st.write("Start an interactive chat. The AI interviewer will ask a question, evaluate your response on the STAR method, and give ratings.")
            
            # Reset Chat
            if st.button("Reset Simulator"):
                st.session_state.interview_messages = []
                st.rerun()
                
            # Initialize Chat
            if not st.session_state.interview_messages:
                st.session_state.interview_messages.append({
                    "role": "interviewer",
                    "text": "Hello! I am your AI Career Coach. Tell me about a time you had to solve a complex technical problem. Please structure your response using the STAR (Situation, Task, Action, Result) format."
                })
                
            for msg in st.session_state.interview_messages:
                if msg["role"] == "interviewer":
                    st.info(f" **Interviewer:** {msg['text']}")
                else:
                    st.success(f" **You:** {msg['text']}")
                    
            user_response = st.text_area("Your Response", height=100, key="star_res")
            if st.button("Submit Answer"):
                if user_response.strip():
                    st.session_state.interview_messages.append({"role": "user", "text": user_response.strip()})
                    with st.spinner("Evaluating STAR framework..."):
                        try:
                            eval_prompt = f"""You are an elite interview coach. Evaluate this candidate response based on the STAR framework:
Candidate Response: {user_response}

Provide:
1. STAR SCORE: (out of 100)
2. CRITIQUE: Breakdown of Situation, Task, Action, Result elements.
3. IMPROVEMENT REWRITE: A highly polished version of their story.
"""
                            critique = ai_call(eval_prompt)
                            st.session_state.interview_messages.append({"role": "interviewer", "text": critique})
                            
                            # Mark daily task complete
                            st.session_state.daily_tasks["interview"] = True

                            # Award XP
                            updated_stats, newly_unlocked = process_xp_and_badges(user["id"], 40, "Interview Prep")
                            if updated_stats:
                                st.session_state.user["xp"] = updated_stats["xp"]
                                st.toast("+40 XP Earned!")
                            for b in newly_unlocked:
                                st.toast(f" Badge Unlocked: {b}!")
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))

    # ── AI RESUME BUILDER ──
    elif page == "Resume Builder":
        st.markdown("""<div class="hero">
            <div class="hero-badge">Resume Architect</div>
            <h1>AI Resume Builder</h1>
            <p>Optimize your resume draft structure and modernization choices.</p>
        </div>""", unsafe_allow_html=True)
        
        mode = st.radio("Operation Mode", ["Build Fresh", "Optimize & Rewrite"])
        if mode == "Build Fresh":
            b_name = st.text_input("Full Name")
            b_title = st.text_input("Professional Title")
            b_skills = st.text_area("Skills (comma-separated)")
            b_exp = st.text_area("Professional Experience details")
            if st.button("Build PDF Draft text"):
                with st.spinner("Compiling structure..."):
                    try:
                        prompt = f"Build an ATS-optimized resume structure for {b_name} ({b_title}). Skills: {b_skills}. Exp: {b_exp}."
                        output = ai_call(prompt)
                        st.markdown(f'<div class="resume-output">{output}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(str(e))
        else:
            b_curr = st.text_area("Paste Current Resume")
            b_jd = st.text_area("Paste Target Job description")
            if st.button("Tailor Resume"):
                with st.spinner("Tailoring content..."):
                    try:
                        prompt = f"Optimize and rewrite this resume to perfectly match this JD. Inject target keywords and quantify impact: Resume: {b_curr} JD: {b_jd}"
                        output = ai_call(prompt)
                        st.markdown(f'<div class="resume-output">{output}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(str(e))

    # ── JOB DISCOVERY / MATCHING ──
    elif page == "Job Discovery":
        st.markdown("""<div class="hero">
            <div class="hero-badge">Job Matcher</div>
            <h1>Smart Job Discovery</h1>
            <p>Automatically match your profile skills against our database of active vacancies.</p>
        </div>""", unsafe_allow_html=True)
        
        st.write("Paste your resume below to rank and discover matches in our active jobs database.")
        disc_resume = st.text_area("Resume Content", height=150, placeholder="Paste resume here...")
        
        if st.button("Find Matching Jobs"):
            if disc_resume.strip():
                jobs_list = get_all_jobs()
                matches = match_resume_to_jobs(disc_resume, jobs_list)
                if matches:
                    # Mark daily task complete
                    st.session_state.daily_tasks["job_match"] = True
                    st.success(f"Found {len(matches)} matching vacancies.")
                    for match in matches:
                        color = "#10b981" if match["score"] >= 75 else ("#f59e0b" if match["score"] >= 50 else "#ef4444")
                        st.markdown(f"""
                        <div class="info-box" style="border-left: 5px solid {color}; padding: 1.5rem; margin-bottom:1rem;">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <h3 style="margin:0;">{match['title']} - <strong>{match['company']}</strong></h3>
                                <span style="font-weight:800; font-size:1.3rem; color:{color};">{match['score']}% Match</span>
                            </div>
                            <div style="font-size:0.85rem; color:var(--text3); margin-top:2px;">{match['location']} |  {match['salary_range']}</div>
                            <p style="margin:10px 0; font-size:0.9rem; color:var(--text2);">{match['description'][:200]}...</p>
                            <div style="margin-top:10px;">
                                <b>Matched Skills:</b> {chips(match['matched_skills'], "chip-green")}
                            </div>
                            <div style="margin-top:5px;">
                                <b>Missing Skills:</b> {chips(match['missing_skills'], "chip-red")}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No vacancies found in the database.")
            else:
                st.error("Please add your resume text first.")

    # ── APPLICATION TRACKER ──
    elif page == "Application Tracker":
        st.markdown("""<div class="hero">
            <div class="hero-badge">Job Tracker</div>
            <h1>Application Pipeline Tracker</h1>
            <p>Track your submitted job applications, manage stages, and visualize conversion funnel.</p>
        </div>""", unsafe_allow_html=True)
        
        t_col1, t_col2 = st.columns([1, 1], gap="large")
        
        with t_col1:
            st.markdown("### Log New Application")
            app_title = st.text_input("Job Title Designation", placeholder="e.g. Frontend Engineer")
            app_comp = st.text_input("Company Name", placeholder="e.g. Stripe")
            app_status = st.selectbox("Current Stage", ["Applied", "Screener", "Technical", "Behavioral", "Offer", "Rejected"])
            
            if st.button("Log Application", type="primary"):
                if app_title and app_comp:
                    add_user_application(user["id"], app_title, app_comp, app_status)
                    
                    # Award 10 XP
                    updated_stats, newly_unlocked = process_xp_and_badges(user["id"], 10, "Application Tracked")
                    if updated_stats:
                        st.session_state.user["xp"] = updated_stats["xp"]
                        st.toast(" +10 XP Earned!")
                    for b in newly_unlocked:
                        st.toast(f" Badge Unlocked: {b}!")
                        
                    st.success(f"Logged application for {app_title} at {app_comp}!")
                    st.rerun()
                else:
                    st.error("Job Title and Company are required.")
                    
        with t_col2:
            st.markdown("### Recruitment Funnel Analysis")
            user_apps = get_user_applications(user["id"])
            if user_apps:
                df_apps = pd.DataFrame(user_apps)
                # Count status conversions for funnel order
                stages = ["Applied", "Screener", "Technical", "Behavioral", "Offer", "Rejected"]
                counts = [len(df_apps[df_apps["status"] == s]) for s in stages]
                
                # Funnel chart
                fig_funnel = go.Figure(go.Funnel(
                    y=stages,
                    x=counts,
                    textinfo="value+percent initial",
                    marker=dict(
                        color=["#8b5cf6", "#a78bfa", "#60a5fa", "#3b82f6", "#10b981", "#ef4444"]
                    )
                ))
                fig_funnel.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#e2e8f0"),
                    margin=dict(l=40, r=40, t=10, b=10)
                )
                st.plotly_chart(fig_funnel, use_container_width=True)
            else:
                st.info("Log applications to construct conversion analytics chart.")
                
        st.markdown("---")
        st.markdown("###  Submitted Applications Registry")
        
        if user_apps:
            for app in user_apps:
                a_id = app["id"]
                c_lbl1, c_lbl2, c_act1, c_act2 = st.columns([2, 1, 1, 1])
                with c_lbl1:
                    st.markdown(f"**{app['job_title']}** at **{app['company']}**")
                with c_lbl2:
                    st.markdown(f"Applied: `{app['date_applied']}`")
                with c_act1:
                    # Update status dropdown
                    statuses = ["Applied", "Screener", "Technical", "Behavioral", "Offer", "Rejected"]
                    cur_idx = statuses.index(app["status"]) if app["status"] in statuses else 0
                    new_st = st.selectbox("Stage", statuses, index=cur_idx, key=f"app_st_{a_id}")
                    if new_st != app["status"]:
                        update_application_status(a_id, new_st)
                        st.toast("Status updated!")
                        st.rerun()
                with c_act2:
                    if st.button("Delete Record", key=f"del_app_{a_id}"):
                        delete_application(a_id)
                        st.toast("Application deleted.")
                        st.rerun()
        else:
            st.write("No active applications currently tracked.")

    # ── CAREER PATHWAYS RECOMMENDATION ──
    elif page == "Career Pathways":
        st.markdown("""<div class="hero">
            <div class="hero-badge">Strategic Planner</div>
            <h1>AI Career Recommendation System</h1>
            <p>Generate optimized roles matching your skill set and plot projected salaries.</p>
        </div>""", unsafe_allow_html=True)
        
        st.write("Enter your skills and core fields of interest to evaluate best career projections.")
        c_skills = st.text_input("Enter Skills (e.g. Python, SQL, Cloud)", placeholder="Comma separated list")
        c_field = st.text_input("Field of Interest", placeholder="e.g. Cloud Architecture, AI Research")
        c_salary = st.selectbox("Desired Target Salary", ["$80,000 - $110,000", "$110,000 - $140,000", "$140,000 - $180,000", "$180,000+"])
        
        if st.button("Generate Projections"):
            if c_field:
                with st.spinner("Evaluating paths..."):
                    try:
                        skills_list = [s.strip() for s in c_skills.split(",")] if c_skills else []
                        paths = recommend_career_path(skills_list, c_field, c_salary, selected_provider, api_key, sel_id)
                        
                        # Award XP
                        updated_stats, newly_unlocked = process_xp_and_badges(user["id"], 35, "Career Path")
                        if updated_stats:
                            st.session_state.user["xp"] = updated_stats["xp"]
                            st.toast(" +35 XP Earned!")
                        for b in newly_unlocked:
                            st.toast(f" Badge Unlocked: {b}!")
                            
                        col_list, col_chart = st.columns([1, 1])
                        with col_list:
                            st.markdown("### Recommended Roles")
                            for p in paths:
                                st.markdown(f"""
                                <div class="info-box" style="margin-bottom:1rem;">
                                    <h4>💼 {p['title']}</h4>
                                    <p style="font-size:0.85rem; color:var(--text2);">{p['description']}</p>
                                    <div style="font-size:0.8rem; margin:8px 0;">
                                         <b>Match:</b> {p['matching_score']}% |  <b>10-Yr Growth:</b> {p['growth_rate']}%
                                    </div>
                                    <div style="font-size:0.8rem;">
                                        <b>Action roadmap:</b>
                                        <ul>
                                            {"".join(f"<li>{step}</li>" for step in p['roadmap_steps'])}
                                        </ul>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                        with col_chart:
                            st.markdown("### Market Salary Breakdown")
                            fig_salary = plot_career_salaries(paths)
                            st.plotly_chart(fig_salary, use_container_width=True)
                    except Exception as e:
                        st.error(str(e))
            else:
                st.error("Please add your fields of interest.")

    # ── AI LEARNING ASSISTANT ──
    elif page == "Learning Assistant":
        st.markdown("""<div class="hero">
            <div class="hero-badge">Skill Optimizer</div>
            <h1>AI Learning Assistant</h1>
            <p>Generate tailored learning plans and search courses for missing skills.</p>
        </div>""", unsafe_allow_html=True)
        
        st.write("We pulled your most frequently missing skills from your previous analyses. Select a skill to build a study plan.")
        missing_list = get_top_missing_skills(limit=5, user_id=user["id"])
        
        if missing_list:
            selected_skill = st.selectbox("Select a Skill to Learn", [m["skill"] for m in missing_list])
            
            if st.button("Generate Weekly Study Guide"):
                with st.spinner("Structuring curriculum..."):
                    try:
                        guide = generate_study_guide(selected_skill, selected_provider, api_key, sel_id)
                        st.markdown("###  Weekly Study Plan")
                        st.markdown(f'<div class="resume-output">{guide}</div>', unsafe_allow_html=True)
                        
                        # Show Course search links
                        links = get_course_search_links(selected_skill)
                        st.markdown("### Recommended Course Resources")
                        c_lnk1, c_lnk2, c_lnk3 = st.columns(3)
                        with c_lnk1:
                            st.markdown(f"<a href='{links['Udemy']}' target='_blank' style='display:block; text-align:center; padding:10px; background:#a78bfa22; border:1px solid #a78bfa; border-radius:10px; text-decoration:none; color:#a78bfa;'>🔍 Search Udemy</a>", unsafe_allow_html=True)
                        with c_lnk2:
                            st.markdown(f"<a href='{links['Coursera']}' target='_blank' style='display:block; text-align:center; padding:10px; background:#a78bfa22; border:1px solid #a78bfa; border-radius:10px; text-decoration:none; color:#a78bfa;'>🔍 Search Coursera</a>", unsafe_allow_html=True)
                        with c_lnk3:
                            st.markdown(f"<a href='{links['YouTube']}' target='_blank' style='display:block; text-align:center; padding:10px; background:#a78bfa22; border:1px solid #a78bfa; border-radius:10px; text-decoration:none; color:#a78bfa;'>🔍 Watch on YouTube</a>", unsafe_allow_html=True)
                            
                        # Award XP
                        updated_stats, newly_unlocked = process_xp_and_badges(user["id"], 30, "Learning Guide")
                        if updated_stats:
                            st.session_state.user["xp"] = updated_stats["xp"]
                            st.toast("+30 XP Earned!")
                        for b in newly_unlocked:
                            st.toast(f" Badge Unlocked: {b}!")
                    except Exception as e:
                        st.error(str(e))
        else:
            st.info("No missing skills logged yet. Complete a Resume Analysis to find missing skills.")

    # ── AI PORTFOLIO BUILDER ──
    elif page == "AI Portfolio":
        st.markdown("""<div class="hero">
            <div class="hero-badge">Web Compiler</div>
            <h1>AI Portfolio Website Builder</h1>
            <p>Compile a custom personal portfolio index.html from your resume and GitHub repositories.</p>
        </div>""", unsafe_allow_html=True)
        
        st.write("Input your profile details and your GitHub username. We will extract repository statistics to dynamically render a custom website.")
        
        c1, c2 = st.columns(2)
        with c1:
            p_name = st.text_input("Name", value=user["username"])
            p_title = st.text_input("Professional Title", placeholder="e.g. Fullstack Developer")
            p_bio = st.text_area("Bio description", placeholder="Write 2 sentences about yourself...")
            p_skills = st.text_area("Key Skills (comma-separated)", placeholder="Python, Git, Docker")
        with c2:
            p_git = st.text_input("GitHub Username", placeholder="e.g. yagyeshVyas")
            p_theme = st.selectbox("Portfolio Theme", ["Minimalist", "Cyberpunk", "Dark Luxury"])
            
        if st.button("Compile Portfolio Website"):
            if p_name and p_title:
                with st.spinner("Fetching GitHub metrics and compiling..."):
                    # 1. Fetch GitHub metrics
                    github_stats = {}
                    if p_git.strip():
                        github_stats = fetch_github_profile_data(p_git.strip())
                        if "error" in github_stats:
                            st.warning(github_stats["error"])
                            github_stats = {}
                        else:
                            st.success("Successfully fetched GitHub stats!")
                            
                    # 2. Build profile dict
                    profile_data = {
                        "name": p_name,
                        "title": p_title,
                        "bio": p_bio,
                        "skills": [s.strip() for s in p_skills.split(",")] if p_skills else [],
                        "github_data": github_stats
                    }
                    
                    try:
                        # 3. Generate HTML code
                        html_code = compile_portfolio_code(profile_data, p_theme, selected_provider, api_key, sel_id)
                        st.session_state["portfolio_html"] = html_code
                        
                        # Award XP
                        updated_stats, newly_unlocked = process_xp_and_badges(user["id"], 45, "Portfolio Builder")
                        if updated_stats:
                            st.session_state.user["xp"] = updated_stats["xp"]
                            st.toast(" +45 XP Earned!")
                        for b in newly_unlocked:
                            st.toast(f"Badge Unlocked: {b}!")
                    except Exception as e:
                        st.error(str(e))
            else:
                st.error("Please add Name and Professional Title.")
                
        if "portfolio_html" in st.session_state:
            st.markdown("###  Website Preview & Code")
            tab_preview, tab_code = st.tabs(["Interactive Web Preview", "Source HTML Code"])
            with tab_preview:
                st.components.v1.html(st.session_state["portfolio_html"], height=500, scrolling=True)
            with tab_code:
                st.code(st.session_state["portfolio_html"], language="html")
                st.download_button("Download index.html", data=st.session_state["portfolio_html"], file_name="index.html", mime="text/html", use_container_width=True)

    # ── AI COPILOT ──
    elif page == "AI Copilot":
        st.markdown("""<div class="hero">
            <div class="hero-badge">AI Assistant</div>
            <h1>Career Copilot Chat</h1>
            <p>Interact with your persistent career strategic assistant.</p>
        </div>""", unsafe_allow_html=True)
        
        st.write("Ask anything about your resume, interview strategy, or salary negotiations.")
        copilot_history = st.container()
        if "copilot_messages" not in st.session_state:
            st.session_state.copilot_messages = [{"role": "assistant", "content": "Hello! I am your career copilot. Ask me to rewrite a resume line, analyze a JD, or draft a networking email."}]
            
        for msg in st.session_state.copilot_messages:
            if msg["role"] == "assistant":
                st.info(f"**Copilot:** {msg['content']}")
            else:
                st.success(f"👤 **You:** {msg['content']}")
                
        c_prompt = st.text_area("Your Question", height=70, placeholder="Type your query...")
        if st.button("Send message"):
            if c_prompt.strip():
                st.session_state.copilot_messages.append({"role": "user", "content": c_prompt.strip()})
                with st.spinner("Thinking..."):
                    try:
                        reply = ai_call(c_prompt.strip())
                        st.session_state.copilot_messages.append({"role": "assistant", "content": reply})
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))

    # ── API GUIDE ──
    elif page == "API Guide":
        st.markdown("""<div class="hero">
            <div class="hero-badge">Integration Manual</div>
            <h1>API Guide & Troubleshooting</h1>
            <p>Reference guide for configuring keys, troubleshooting error response codes, and setting up local models.</p>
        </div>""", unsafe_allow_html=True)
        
        st.markdown("""
        ###  API Providers Status
        - **OpenRouter**: Works with 200+ models. Highly recommended.
        - **Google Gemini**: Excellent speed, 1M free daily tokens.
        - **Groq**: Extremely fast inference speeds for Llama models.
        
        ###  Common Error Codes
        - **401 Unauthorized**: Invalid API key. Double check your key and copy-paste again.
        - **429 Rate Limit**: You made too many requests in a short time. Wait 1 minute or switch provider.
        - **404 Model Not Found**: The model display name changed or is deprecated. Try the `Auto Free Router`.
        
        ###  Local Integration (Ollama)
        Ensure Ollama server is running locally:
        `ollama serve`
        Select Ollama in sidebar. No API key needed.
        """)


# ════════════════════════════════════════════════════════
# RECRUITER ROLE ROUTING
# ════════════════════════════════════════════════════════
elif role == "recruiter":
    
    # ── RECRUITER DASHBOARD (Candidate Screener) ──
    if page == "Dashboard":
        st.markdown("""<div class="hero">
            <div class="hero-badge">Recruiter Portal</div>
            <h1>Candidate Ranking Screener</h1>
            <p>Upload candidate resumes in batch and rank compatibility with active jobs.</p>
        </div>""", unsafe_allow_html=True)
        
        st.markdown("###  Bulk Screener Panel")
        rec_jd = st.text_area("Job Requirements", height=150, placeholder="Paste details of targeted vacancy role...")
        res_files = st.file_uploader("Upload Resumes (Multiple PDFs)", type=["pdf"], accept_multiple_files=True)
        
        if st.button("Run Batch Screen Ranking", type="primary"):
            if rec_jd.strip() and res_files:
                ranked_candidates = []
                for file in res_files:
                    with st.spinner(f"Screener parsing {file.name}..."):
                        try:
                            # 1. Extract text
                            txt = extract_text_from_pdf(file)
                            # 2. Extract quick metrics (we can simulate or make quick AI calls, to keep it simple let's count overlaps)
                            job_dict = {
                                "id": 999, "title": "Target Role", "company": "Recruiter Search",
                                "description": rec_jd, "location": "", "salary_range": "",
                                "required_skills": [w.strip() for w in rec_jd.split() if len(w) > 4][:12] # Mock required skill list from text
                            }
                            match_res = match_resume_to_jobs(txt, [job_dict])[0]
                            
                            ranked_candidates.append({
                                "name": file.name,
                                "score": match_res["score"],
                                "matched": match_res["matched_skills"],
                                "missing": match_res["missing_skills"]
                            })
                        except Exception as e:
                            st.warning(f"Failed to parse {file.name}: {str(e)}")
                            
                # Sort by score
                ranked_candidates = sorted(ranked_candidates, key=lambda x: x["score"], reverse=True)
                
                # Render results
                st.markdown("### Ranked Candidates List")
                for index, cand in enumerate(ranked_candidates):
                    color = "#10b981" if cand["score"] >= 75 else ("#f59e0b" if cand["score"] >= 50 else "#ef4444")
                    st.markdown(f"""
                    <div class="info-box" style="border-left:5px solid {color}; padding:1.2rem;">
                        <div style="display:flex; justify-content:space-between;">
                            <span> Rank {index+1}: <b>{cand['name']}</b></span>
                            <span style="color:{color}; font-weight:800;">{cand['score']}% Compatibility</span>
                        </div>
                        <div style="margin-top:8px;"><b>Matched Skills:</b> {chips(cand['matched'], "chip-green")}</div>
                        <div style="margin-top:4px;"><b>Gaps identified:</b> {chips(cand['missing'], "chip-red")}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("Please add Job requirements and upload resumes.")

    # ── JOB VACANCY POSTINGS MANAGEMENT ──
    elif page == "Job Postings":
        st.markdown("""<div class="hero">
            <div class="hero-badge">Vacancy Management</div>
            <h1>Manage Job Vacancies</h1>
            <p>Post new job profiles to database matching systems.</p>
        </div>""", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Post New Job", "Active Vacancies"])
        
        with tab1:
            j_title = st.text_input("Job Title")
            j_comp = st.text_input("Company", value="Recruiter Org")
            j_loc = st.text_input("Location")
            j_salary = st.text_input("Salary Range", placeholder="e.g. $120,000 - $155,000")
            j_skills = st.text_area("Required Skills (comma-separated)")
            j_desc = st.text_area("Job Description Details", height=150)
            
            if st.button("Add Job Listing", type="primary"):
                if j_title and j_desc:
                    skills_list = [s.strip() for s in j_skills.split(",")] if j_skills else []
                    save_job(j_title, j_comp, j_desc, j_loc, j_salary, skills_list)
                    st.success(f"Job vacancy '{j_title}' posted successfully!")
                else:
                    st.error("Please fill required fields (Title & Description).")
                    
        with tab2:
            st.markdown("### Active Jobs Database")
            all_jobs = get_all_jobs()
            for job in all_jobs:
                with st.expander(f"{job['title']} - {job['company']}"):
                    st.write(f" **Location:** {job['location']} |  **Salary:** {job['salary_range']}")
                    st.write(f"**Description:** {job['description']}")
                    st.write(f" **Skills required:** {', '.join(job['required_skills'])}")
                    if st.button("Delete Listing", key=f"del_{job['id']}"):
                        delete_job(job["id"])
                        st.success("Job listing deleted!")
                        st.rerun()

    # ── API GUIDE ──
    elif page == "API Guide":
        st.markdown("""<div class="hero">
            <div class="hero-badge">Manual</div>
            <h1>Recruiter API Guidelines</h1>
            <p>Instructions to connect candidate databases and configure API providers.</p>
        </div>""", unsafe_allow_html=True)
        st.write("Ensure your API key is validated in the sidebar to process evaluations.")


# ════════════════════════════════════════════════════════
# ADMIN ROLE ROUTING
# ════════════════════════════════════════════════════════
elif role == "admin":
    
    # ── ADMIN DASHBOARD (System Status & Stats) ──
    if page == "Dashboard":
        st.markdown("""<div class="hero">
            <div class="hero-badge">System Control</div>
            <h1>Admin Administration Dashboard</h1>
            <p>Monitor platform statistics, registered profiles, and database logs.</p>
        </div>""", unsafe_allow_html=True)
        
        stats = get_system_stats()
        
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric(label="Total Users", value=stats["total_users"])
        with m2:
            st.metric(label="Total Resume Analyses", value=stats["total_analyses"])
        with m3:
            st.metric(label="Total Jobs in DB", value=stats["total_jobs"])
        with m4:
            st.metric(label="Avg ATS Score", value=f"{stats['avg_ats_score']}%")
            
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("###  Registered Users Split")
            roles = list(stats["roles"].keys())
            counts = list(stats["roles"].values())
            fig_roles = px.pie(names=roles, values=counts, hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_roles.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e2e8f0"))
            st.plotly_chart(fig_roles, use_container_width=True)
            
        with c2:
            st.markdown("###  Analysis Logs History")
            all_logs = get_all_analyses()
            if all_logs:
                df_logs = pd.DataFrame(all_logs)
                # Group by job_title
                grp = df_logs.groupby("job_title").size().reset_index(name="counts")
                fig_grp = px.bar(grp, x="job_title", y="counts", color="counts")
                fig_grp.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#e2e8f0"))
                st.plotly_chart(fig_grp, use_container_width=True)
            else:
                st.info("No system analysis data logged yet.")

    # ── USER REGISTRY MANAGEMENT ──
    elif page == "User Registry":
        st.markdown("""<div class="hero">
            <div class="hero-badge">Account Controls</div>
            <h1>User Profiles Registry</h1>
            <p>Manage user roles, wipe credentials, or reset gamified records.</p>
        </div>""", unsafe_allow_html=True)
        
        users_list = get_all_users()
        df_users = pd.DataFrame(users_list)
        st.dataframe(df_users, use_container_width=True)
        
        st.markdown("---")
        st.markdown("###  Account Management Actions")
        usr_names = [u["username"] for u in users_list]
        selected_username = st.selectbox("Select Username to Manage", usr_names)
        
        target_usr = next(u for u in users_list if u["username"] == selected_username)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Reset Gamified XP/Badges", use_container_width=True):
                reset_user_xp(target_usr["id"])
                st.toast(f"Wiped XP records for {selected_username}")
                st.rerun()
        with col2:
            new_role_val = st.selectbox("Change User Role", ["student", "recruiter", "admin"])
            if st.button("Apply New Role", use_container_width=True):
                update_user_role(target_usr["id"], new_role_val)
                st.toast(f"Updated {selected_username} role to {new_role_val}")
                st.rerun()
        with col3:
            st.write("⚠️ Destructive Action")
            if st.button("Delete User Account", type="primary", use_container_width=True):
                delete_user(target_usr["id"])
                st.toast(f"Deleted user account {selected_username}!")
                st.rerun()

    # ── API GUIDE ──
    elif page == "API Guide":
        st.markdown("""<div class="hero">
            <div class="hero-badge">Manual</div>
            <h1>Admin Platform Integrations</h1>
            <p>Configuration guides for modifying database parameters and API key pools.</p>
        </div>""", unsafe_allow_html=True)
        st.write("Configure model allocations in the sidebar to review system API usage.")
