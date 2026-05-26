"""
app.py - AI Career Suite | Dark Luxury UI
Author: Yagyesh Vyas | github.com/yagyeshVyas
"""

import streamlit as st
import pandas as pd
from providers import PROVIDERS, call_api
from analyzer import (
    extract_text_from_pdf, analyze_resume,
    get_score_label
)
from database import (
    init_db, save_analysis, get_all_analyses,
    get_top_missing_skills, get_score_trend, delete_analysis
)
import plotly.express as px
import plotly.graph_objects as go
from scrape_job import fetch_job_description

st.set_page_config(
    page_title="AI Career Suite",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

/* ── Animations ── */
/* ── 3D Mesh Gradient Background ── */
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

/* ── Floating 3D Grid ── */
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

/* ── Hero — 3D Parallax Style ── */
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

/* ── Score Cards — 3D Tilt ── */
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

/* ── UI Elements — Depth ── */
.info-box, .win-box, .success-box, .danger-box {
    border-radius:14px; padding:1.2rem 1.5rem; margin:0.8rem 0;
    transition:all 0.3s ease; transform-style:preserve-3d;
}
.info-box:hover { transform:translateX(5px) translateZ(10px); background:rgba(139,92,246,0.1); }

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
.resume-output:hover { transform:rotateY(-1deg) rotateX(1deg) scale(1.005); border-color:var(--purple); }

/* ── Staggered 3D Animations ── */
div[data-testid="stVerticalBlock"] > div { animation:fade-in 0.8s cubic-bezier(0.22, 1, 0.36, 1) backwards; }
div[data-testid="stVerticalBlock"] > div:nth-child(1) { animation-delay:0.1s; }
div[data-testid="stVerticalBlock"] > div:nth-child(2) { animation-delay:0.2s; }
div[data-testid="stVerticalBlock"] > div:nth-child(3) { animation-delay:0.3s; }
div[data-testid="stVerticalBlock"] > div:nth-child(4) { animation-delay:0.4s; }
div[data-testid="stVerticalBlock"] > div:nth-child(5) { animation-delay:0.5s; }

/* ── Form Controls — 3D Glow ── */
.stTextInput>div>div>input, .stTextArea>div>div>textarea {
    border-radius:14px !important; padding:12px 18px !important;
    background:rgba(255,255,255,0.03) !important;
    transition:all 0.3s !important;
}
.stTextInput>div>div>input:hover, .stTextArea>div>div>textarea:hover {
    background:rgba(255,255,255,0.05) !important;
    border-color:var(--border2) !important;
}

/* ── Buttons — Neo-3D ── */
.stButton>button {
    background:linear-gradient(135deg,#7c3aed,#6366f1) !important;
    border:1px solid rgba(255,255,255,0.1) !important;
    border-radius:15px !important; padding:0.8rem 2.2rem !important;
    transform:translateZ(0); transition:all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
}
.stButton>button:hover {
    transform:translateY(-4px) translateZ(15px) !important;
    box-shadow:0 15px 30px rgba(124,58,237,0.4), 0 0 10px rgba(124,58,237,0.2) !important;
    background:linear-gradient(135deg,#8b5cf6,#4f46e5) !important;
}
.stButton>button:active { transform:translateY(0) scale(0.98) !important; }

/* ── Metrics — Elevated ── */
[data-testid="stMetric"] {
    background:rgba(255,255,255,0.02); border:1px solid var(--border);
    border-radius:18px; padding:1.2rem; transform-style:preserve-3d;
    transition:all 0.3s ease;
}
[data-testid="stMetric"]:hover {
    transform:translateY(-5px) translateZ(10px);
    border-color:var(--purple);
    background:rgba(255,255,255,0.04);
}

#MainMenu, footer, header { visibility:hidden; }
::-webkit-scrollbar { width:8px; }
::-webkit-scrollbar-thumb { background:rgba(139,92,246,0.3); border-radius:10px; }
::-webkit-scrollbar-thumb:hover { background:rgba(139,92,246,0.5); }
</style>
""", unsafe_allow_html=True)

init_db()

# ── SESSION STATE INIT — persists keys across all rerenders ──
if "api_keys"not in st.session_state:
    st.session_state.api_keys = {}   # {provider_name: key_string}
if "prev_provider"not in st.session_state:
    st.session_state.prev_provider = None

# ── SIDEBAR ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='font-family:Syne,sans-serif;font-size:1.3rem;font-weight:800;background:linear-gradient(135deg,#a78bfa,#60a5fa);-webkit-background-clip:text;-webkit-text-fill-color:transparent'>AI Career Suite</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.72rem;color:#475569;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:1.5rem'>13+ AI Providers · NVIDIA NIM</div>", unsafe_allow_html=True)

    # ── Provider Selector ──
    st.markdown("**AI Provider**")
    selected_provider = st.selectbox("Hidden Label", list(PROVIDERS.keys()),
        label_visibility="collapsed", key="provider_sel"
    )
    pinfo = PROVIDERS[selected_provider]

    # Show provider info
    free_tier_color = "#10b981"if ""in pinfo["free_tier"] else "#f59e0b"
    st.markdown(f"""<div class="api-box"style="font-size:0.76rem;line-height:1.8">
    <b>{pinfo['description']}</b><br>
    <span style="color:{free_tier_color}">{pinfo['free_tier']}</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── API Key — persisted per provider in session_state ──
    st.markdown(f"**{selected_provider} API Key**")

    # Pre-fill from saved key for this provider
    saved_key = st.session_state.api_keys.get(selected_provider, "")

    entered_key = st.text_input("Hidden Label",
        value=saved_key,
        type="password",
        placeholder=pinfo["placeholder"],
        label_visibility="collapsed",
        key=f"apikey_{selected_provider}"  # unique key per provider — never resets
    )

    # Save key back whenever it changes
    if entered_key:
        st.session_state.api_keys[selected_provider] = entered_key.strip()

    # Local providers don't need a key
    is_local = pinfo.get("local_only", False)
    if is_local:
        st.session_state.api_keys[selected_provider] = "local"

    # Always use the session-stored key (survives rerenders)
    api_key = st.session_state.api_keys.get(selected_provider, "").strip()

    if is_local:
        st.markdown("""<div style="background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.25);border-radius:8px;padding:8px 10px;font-size:0.75rem;color:#10b981;margin-top:4px">
        <b>No API key needed!</b> Runs 100% on your machine.
        </div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="api-box">Download: <a href="{pinfo['get_key_url']}"target="_blank">{pinfo['get_key_url'].replace('https://','')}</a></div>""", unsafe_allow_html=True)
    elif api_key:
        st.markdown(f"""<div style="background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.25);border-radius:8px;padding:6px 10px;font-size:0.75rem;color:#10b981;margin-top:4px">
        Key saved — <code style="font-size:0.7rem">{api_key[:8]}...{api_key[-4:]}</code>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="api-box">Get free key: <a href="{pinfo['get_key_url']}"target="_blank">{pinfo['get_key_url'].replace('https://','')}</a></div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Model Selector ──
    free_models, paid_models = pinfo["free_models"], pinfo["paid_models"]
    has_free = len(free_models) > 0
    has_paid = len(paid_models) > 0

    if has_free and has_paid:
        tier = st.radio("**Model Tier**", ["Free", "Paid"], horizontal=True,
                        key=f"tier_{selected_provider}")
        if tier == "Free":
            st.markdown('<span class="free-badge">✓ No credits needed</span>', unsafe_allow_html=True)
            model_opts = list(free_models.keys())
        else:
            st.markdown('<span class="paid-badge">Credits required</span>', unsafe_allow_html=True)
            model_opts = list(paid_models.keys())
    elif has_free:
        st.markdown('<span class="free-badge">✓ All models FREE</span>', unsafe_allow_html=True)
        model_opts = list(free_models.keys())
    elif has_paid:
        st.markdown('<span class="paid-badge">Paid models only</span>', unsafe_allow_html=True)
        model_opts = list(paid_models.keys())
    else:
        model_opts = ["No models available"]

    sel_name = st.selectbox("Hidden Label", model_opts, label_visibility="collapsed",
                            key=f"model_{selected_provider}")
    all_provider_models = {**free_models, **paid_models}
    sel_id = all_provider_models.get(sel_name, sel_name)

    # Custom model name for Ollama
    if sel_id == "__custom__"or (is_local and "Ollama"in selected_provider):
        custom_model = st.text_input(
            "Custom model name:",
            placeholder="e.g. llama3.2, mistral, phi4, deepseek-r1:7b",
            key="ollama_custom_model"
        )
        if custom_model.strip():
            sel_id = custom_model.strip()
        elif sel_id == "__custom__":
            sel_id = "llama3.2" # safe fallback

    # Local-only warning on Streamlit Cloud
    if is_local:
        st.markdown("""<div style="background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.25);border-radius:8px;padding:8px 10px;font-size:0.74rem;color:#fbbf24;margin-top:6px;line-height:1.6">
        <b>Local only!</b> This works when you run<br>
        <code style="font-size:0.7rem">streamlit run app.py</code> on your own machine.<br>
        Won't work on Streamlit Cloud.
        </div>""", unsafe_allow_html=True)

    # ── Key status indicator ──
    if not api_key:
        st.markdown("""<div style="background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.25);border-radius:8px;padding:8px 10px;font-size:0.78rem;color:#f87171;margin-top:6px">
        <b>No API key entered.</b><br>
        Paste your key above — it stays saved even when you switch pages or models!
        </div>""", unsafe_allow_html=True)

    # ── Saved keys summary (all providers) ──
    saved_providers = [p for p, k in st.session_state.api_keys.items() if k]
    if len(saved_providers) > 1:
        st.markdown(f"""<div style="background:rgba(139,92,246,0.06);border:1px solid rgba(139,92,246,0.15);border-radius:8px;padding:6px 10px;font-size:0.73rem;color:#a78bfa;margin-top:4px">
        Keys saved for {len(saved_providers)} providers
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    page = st.radio("**Navigate**", [
        "Analyzer", "Cover Letter",
        "Interview Prep", "Resume Builder",
        "Job Discovery", "AI Copilot",
        "Dashboard", "API Guide", "How to Use", "About"
    ], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("<div style='font-size:0.72rem;color:#475569;text-align:center;line-height:1.8'>Built by <b style='color:#7c3aed'>Yagyesh Vyas</b><br>Python · 10+ AI APIs · SQLite · Streamlit</div>", unsafe_allow_html=True)


# ── HELPERS ──────────────────────────────────────────────
def chips(items, cls="chip-green"):
    if not items:
        return "<span style='color:#475569;font-style:italic;font-size:0.82rem'>None found</span>"
    return '<div class="chips">'+ "".join(f'<span class="chip {cls}">{i}</span>'for i in items) + '</div>'


def score_card(score, title):
    cls = "green"if score >= 75 else ("amber"if score >= 50 else "red")
    st.markdown(f"""<div class="score-wrap {cls}">
        <div class="score-title">{title}</div>
        <div class="score-number {cls}">{score}</div>
        <div class="score-label">out of 100</div>
        <span class="score-badge {cls}">{get_score_label(score)}</span>
    </div>""", unsafe_allow_html=True)
    st.progress(score / 100)


def ai_call(prompt, temperature=0.7, max_tokens=2500):
    if not api_key:
        raise ValueError(
            "No API key entered!\n\n"
            "Paste your key in the sidebar ← under your provider.\n"
            "Get a FREE key at openrouter.ai/keys (takes 2 minutes, no credit card)"
        )
    return call_api(selected_provider, api_key, sel_id, prompt, temperature, max_tokens)


# ════════════════════════════════════════════════════════
# RESUME ANALYZER
# ════════════════════════════════════════════════════════
if page == "Analyzer":
    st.markdown("""<div class="hero"><div class="hero-badge">ATS · Match Score · Interview Probability · Deep Analysis</div>
    <h1>AI Career Suite</h1>
    <p>Upload your resume, paste any job description — get a senior recruiter's verdict with competitive positioning in seconds</p></div>""", unsafe_allow_html=True)

    if not api_key:
        st.warning("Enter your free OpenRouter API key in the sidebar → openrouter.ai/keys")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="section-title">Your Resume</div>', unsafe_allow_html=True)
        rtype = st.radio("Hidden Label", ["Upload PDF", "Paste Text"], horizontal=True, label_visibility="collapsed", key="an_rt")
        resume_text = ""
        resume_file = ""
        if rtype == "Upload PDF":
            up = st.file_uploader("Hidden Label", type=["pdf"], label_visibility="collapsed", key="an_pdf")
            if up:
                try:
                    resume_text = extract_text_from_pdf(up)
                    resume_file = up.name
                    st.success(f"Extracted {len(resume_text.split())} words from **{up.name}**")
                    with st.expander("Preview"):
                        st.text(resume_text[:600] + "..."if len(resume_text) > 600 else resume_text)
                except ValueError as e:
                    st.error(str(e))
        else:
            resume_text = st.text_area("Hidden Label", height=220, placeholder="Paste your full resume text here...", label_visibility="collapsed", key="an_paste")
            resume_file = "pasted.txt"
    with c2:
        st.markdown('<div class="section-title">Job Details</div>', unsafe_allow_html=True)
        jt = st.text_input("Job Title", placeholder="e.g. Data Engineer, AI Engineer", value=st.session_state.get("az_title", ""))
        co = st.text_input("Company", placeholder="e.g. Google, Amazon, TCS", value=st.session_state.get("az_company", ""))
        j_mode = st.radio("Provide Job Description:", ["Paste Text", "Scrape URL"], horizontal=True)
        if j_mode == "Scrape URL":
            url = st.text_input("Job Link URL", placeholder="https://greenhouse.io/... (Many job boards supported)")
            if url and st.button("Scrape Page"):
                with st.spinner("Extracting..."):
                    scrape_data = fetch_job_description(url)
                    st.session_state["fetched_jd"] = scrape_data["text"]
                    if scrape_data["title"]: st.session_state["az_title"] = scrape_data["title"]
                    if scrape_data["company"]: st.session_state["az_company"] = scrape_data["company"]
                    st.rerun()
            jd = st.text_area("Extracted Job Context", value=st.session_state.get("fetched_jd", ""), height=150)
        else:
            jd = st.text_area("Job Description", height=180, placeholder="Paste the full job posting here — requirements, responsibilities, qualifications...")

    st.markdown("")
    if st.button("Analyze My Resume", type="primary", use_container_width=True, disabled=not api_key):
        if not api_key:
            st.error("No API key! Paste your key in the sidebar ← first.")
        elif not resume_text.strip():
            st.error("Please provide your resume.")
        elif not jd.strip():
            st.error("Please paste the job description.")
        elif len(jd) < 50:
            st.error("Job description too short — paste the full posting.")
        else:
            with st.spinner("Analyzing with senior recruiter-level AI..."):
                try:
                    result = analyze_resume(api_key, sel_id, resume_text, jd, jt, co, selected_provider)
                    result.update({"resume_filename": resume_file, "job_title": jt, "company_name": co, "word_count": len(resume_text.split())})
                    save_analysis(result)
                    st.session_state["last_result"] = result
                    st.success("Analysis complete!")
                except ValueError as e:
                    st.error(f"{e}")

    if "last_result"in st.session_state:
        r = st.session_state["last_result"]
        st.markdown("---")
        if r.get("job_title"):
            st.markdown(f"<h3 style='color:#e2e8f0;font-family:Syne'>Results — {r['job_title']}{'@ '+r['company_name'] if r.get('company_name') else ''}</h3>", unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1:
            score_card(r["ats_score"], "ATS Score")
        with s2:
            score_card(r["match_score"], "Job Match")
        with s3:
            score_card(r.get("hire_probability", 0), "Interview Chance")
        st.markdown(f'<div class="summary-box"><strong>AI Verdict:</strong> {r["overall_summary"]}</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown('<div class="section-title">Matched Skills</div>', unsafe_allow_html=True)
            st.markdown(chips(r["matched_skills"], "chip-green"), unsafe_allow_html=True)
            st.markdown('<div class="section-title">Strengths</div>', unsafe_allow_html=True)
            for s in r.get("strengths", []):
                st.markdown(f'<div class="info-box">{s}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="section-title">Missing Skills</div>', unsafe_allow_html=True)
            st.markdown(chips(r["missing_skills"], "chip-red"), unsafe_allow_html=True)
            st.markdown('<div class="section-title">Improvements</div>', unsafe_allow_html=True)
            for tip in r.get("improvements", []):
                st.markdown(f'<div class="info-box">{tip}</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">ATS Keywords to Add</div>', unsafe_allow_html=True)
        st.markdown(chips(r.get("keyword_suggestions", []), "chip-blue"), unsafe_allow_html=True)
        if r.get("quick_wins"):
            st.markdown('<div class="section-title">Quick Wins — Fix in 10 Minutes</div>', unsafe_allow_html=True)
            for w in r["quick_wins"]:
                st.markdown(f'<div class="win-box">{w}</div>', unsafe_allow_html=True)
        if r.get("red_flags"):
            st.markdown('<div class="section-title">Recruiter Red Flags</div>', unsafe_allow_html=True)
            for f in r["red_flags"]:
                st.markdown(f'<div class="danger-box">{f}</div>', unsafe_allow_html=True)
        if r.get("salary_insight"):
            st.markdown(f'<div class="success-box"><strong>Salary Insight:</strong> {r["salary_insight"]}</div>', unsafe_allow_html=True)
        with st.expander("Experience & Education Details"):
            e1, e2 = st.columns(2)
            with e1:
                st.markdown("**Experience Gap**")
                st.info(r.get("experience_gap", "N/A"))
            with e2:
                st.markdown("**Education Match**")
                st.info(r.get("education_match", "N/A"))
        st.markdown("---")
        report = f"""AI RESUME ANALYSIS REPORT\n{'='*50}
Job: {r.get('job_title','N/A')} @ {r.get('company_name','N/A')}
ATS: {r['ats_score']}/100 | Match: {r['match_score']}/100 | Interview: {r.get('hire_probability',0)}/100
\nSUMMARY\n{r['overall_summary']}
\nMATCHED: {', '.join(r['matched_skills'])}
MISSING:  {', '.join(r['missing_skills'])}
KEYWORDS: {', '.join(r.get('keyword_suggestions',[]))}
\nSTRENGTHS\n{chr(10).join('• '+s for s in r['strengths'])}
\nIMPROVEMENTS\n{chr(10).join('• '+s for s in r['improvements'])}
\nQUICK WINS\n{chr(10).join('• '+s for s in r.get('quick_wins',[]))}
\nRED FLAGS\n{chr(10).join('• '+s for s in r.get('red_flags',[]))}
\nSALARY: {r.get('salary_insight','N/A')}
EXPERIENCE: {r.get('experience_gap','N/A')}
EDUCATION: {r.get('education_match','N/A')}"""
        st.download_button("Download Full Report", data=report, file_name=f"analysis_{(r.get('job_title','role')).replace(' ', '_')}.txt", mime="text/plain", use_container_width=True)

        # ── DEEP ANALYSIS — Follow-up AI Call ──
        st.markdown('---')
        st.markdown('<div class="section-title">Deep Analysis — Advanced Insights</div>', unsafe_allow_html=True)
        st.markdown("""<div class="info-box"><strong>Go deeper:</strong> Generate competitive positioning, section-by-section resume grading, and personalized rewrite suggestions powered by AI.</div>""", unsafe_allow_html=True)

        da1, da2, da3 = st.columns(3)
        with da1:
            if st.button("Competitive Positioning", use_container_width=True, key="deep_comp", disabled=not api_key):
                with st.spinner("Analyzing your competitive position..."):
                    try:
                        comp = ai_call(f"""You are a senior career strategist. Based on this resume and job description, provide a COMPETITIVE POSITIONING ANALYSIS.

RESUME: {r.get('_resume_text', resume_text)}
JOB: {r.get('job_title','the role')} at {r.get('company_name','the company')}
JD: {jd}

Provide:
1. POSITIONING STATEMENT: One powerful sentence describing this candidate's unique value proposition
2. TOP 3 DIFFERENTIATORS: What sets this candidate apart from other applicants
3. COMPETITIVE WEAKNESSES: 2-3 areas where other candidates likely beat them
4. MARKET DEMAND: How in-demand is this skill set right now (High/Medium/Low with explanation)
5. CAREER TRAJECTORY: Where this person should aim in 2-3 years based on their trajectory
6. NETWORKING STRATEGY: 3 specific actions to get noticed by hiring managers at {r.get('company_name','this company')}
7. HIDDEN STRENGTHS: 2 skills/experiences in the resume that the candidate probably undervalues

Be specific, actionable, and reference actual resume content.""", temperature=0.5, max_tokens=1500)
                        st.markdown(f'<div class="resume-output">{comp}</div>', unsafe_allow_html=True)
                        st.download_button("Download Competitive Analysis", data=comp, file_name="competitive_analysis.txt", mime="text/plain", use_container_width=True, key="dl_comp")
                    except Exception as e:
                        st.error(f"{e}")

        with da2:
            if st.button("Section-by-Section Grade", use_container_width=True, key="deep_grade", disabled=not api_key):
                with st.spinner("Grading each resume section..."):
                    try:
                        grade = ai_call(f"""You are a professional resume reviewer. Grade each section of this resume for the target job.

RESUME: {r.get('_resume_text', resume_text)}
TARGET: {r.get('job_title','the role')} at {r.get('company_name','the company')}

For EACH section below, give: Grade (A/B/C/D/F), Score (0-100), What's Good, What to Fix, Rewritten Example.

Sections to grade:
1. CONTACT INFO & HEADER
2. PROFESSIONAL SUMMARY / OBJECTIVE
3. WORK EXPERIENCE (bullet quality, action verbs, metrics)
4. SKILLS SECTION (organization, relevance, ATS keywords)
5. EDUCATION
6. PROJECTS / PORTFOLIO
7. CERTIFICATIONS
8. OVERALL FORMATTING & STRUCTURE

For each section that scores below B, provide a SPECIFIC rewritten example that would score A.
End with an OVERALL GPA across all sections.""", temperature=0.4, max_tokens=2500)
                        st.markdown(f'<div class="resume-output">{grade}</div>', unsafe_allow_html=True)
                        st.download_button("Download Section Grades", data=grade, file_name="section_grades.txt", mime="text/plain", use_container_width=True, key="dl_grade")
                    except Exception as e:
                        st.error(f"{e}")

        with da3:
            if st.button("AI Rewrite Suggestions", use_container_width=True, key="deep_rewrite", disabled=not api_key):
                with st.spinner("Generating rewrite suggestions..."):
                    try:
                        rewrite = ai_call(f"""You are the world's best resume writer. Rewrite the WEAKEST parts of this resume to score 95+ ATS.

RESUME: {r.get('_resume_text', resume_text)}
TARGET JOB: {r.get('job_title','the role')}
MISSING SKILLS: {', '.join(r.get('missing_skills',[]))}
KEYWORDS TO ADD: {', '.join(r.get('keyword_suggestions',[]))}

Provide:
1. REWRITTEN PROFESSIONAL SUMMARY (3 powerful sentences targeting this exact job)
2. TOP 5 BULLET REWRITES (take the weakest bullets → rewrite with [Power Verb] + [Action] + [Tool] + [Measurable Result])
3. SKILLS SECTION REWRITE (organized by category, critical skills first, all missing keywords injected)
4. 3 NEW BULLETS TO ADD (based on likely experience that isn't highlighted enough)
5. LINKEDIN HEADLINE (120 chars max, keyword-rich)
6. LINKEDIN SUMMARY (3 sentences, different from resume summary)

Make every word count. Use exact keywords from the job description.""", temperature=0.4, max_tokens=2000)
                        st.markdown(f'<div class="resume-output">{rewrite}</div>', unsafe_allow_html=True)
                        st.download_button("Download Rewrite Suggestions", data=rewrite, file_name="rewrite_suggestions.txt", mime="text/plain", use_container_width=True, key="dl_rewrite")
                    except Exception as e:
                        st.error(f"{e}")


# ════════════════════════════════════════════════════════
# COVER LETTER
# ════════════════════════════════════════════════════════
elif page == "Cover Letter":
    st.markdown("""<div class="hero"><div class="hero-badge">Cover Letter · Follow-Up Email · Thank You Note · LinkedIn Message</div>
    <h1>Smart Letter Generator</h1>
    <p>Generate any professional document — cover letters, follow-up emails, thank-you notes, and LinkedIn outreach messages</p></div>""", unsafe_allow_html=True)
    if not api_key:
        st.warning("Enter your free API key in the sidebar")

    # ── Document Type Selector ──
    st.markdown('<div class="section-title">Document Type</div>', unsafe_allow_html=True)
    doc_type = st.radio("Hidden Label", ["Cover Letter", "Follow-Up Email", "Thank You Note", "LinkedIn Message", "Cold Outreach Email"], horizontal=True, label_visibility="collapsed", key="doc_type")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="section-title">Your Resume</div>', unsafe_allow_html=True)
        ct = st.radio("Hidden Label", ["Upload PDF", "Paste Text"], horizontal=True, label_visibility="collapsed", key="cl_rt")
        cl_r = ""
        if ct == "Upload PDF":
            up = st.file_uploader("Hidden Label", type=["pdf"], label_visibility="collapsed", key="cl_pdf")
            if up:
                try:
                    cl_r = extract_text_from_pdf(up)
                    st.success(f"{len(cl_r.split())} words extracted")
                except ValueError as e:
                    st.error(str(e))
        else:
            cl_r = st.text_area("Hidden Label", height=200, placeholder="Paste resume...", label_visibility="collapsed", key="cl_paste")
    with c2:
        st.markdown('<div class="section-title">Job Details</div>', unsafe_allow_html=True)
        cl_jt = st.text_input("Job Title", placeholder="e.g. Data Engineer", value=st.session_state.get("cl_title", ""), key="cl_jt")
        cl_co = st.text_input("Company", placeholder="e.g. Google", value=st.session_state.get("cl_company", ""), key="cl_co")
        cl_hm = st.text_input("Hiring Manager (optional)", placeholder="e.g. Sarah Johnson", key="cl_hm")
        
        cl_j_mode = st.radio("Provide Job Description:", ["Paste Text", "Scrape URL"], horizontal=True, key="cl_j_mode")
        if cl_j_mode == "Scrape URL":
            cl_url = st.text_input("Job Link URL", placeholder="https://greenhouse.io/...", key="cl_url")
            if cl_url and st.button("Scrape Page", key="cl_scrape"):
                with st.spinner("Extracting..."):
                    scrape_data = fetch_job_description(cl_url)
                    st.session_state["cl_fetched_jd"] = scrape_data["text"]
                    if scrape_data["title"]: st.session_state["cl_title"] = scrape_data["title"]
                    if scrape_data["company"]: st.session_state["cl_company"] = scrape_data["company"]
                    st.rerun()
            cl_jd = st.text_area("Extracted Job Context", value=st.session_state.get("cl_fetched_jd", ""), height=100, key="cl_jd")
        else:
            cl_jd = st.text_area("Job Description", height=140, key="cl_jd_paste", placeholder="Paste job posting here...")

    # ── Extra options based on doc type ──
    if doc_type == "Follow-Up Email":
        st.markdown('<div class="section-title">Follow-Up Details</div>', unsafe_allow_html=True)
        fu_context = st.radio("Hidden Label", ["After applying (no response)", "After phone screen", "After interview", "After rejection (re-engage)"], horizontal=True, label_visibility="collapsed", key="fu_ctx")
        fu_days = st.slider("Days since last contact", 1, 30, 7, key="fu_days")
    elif doc_type == "Thank You Note":
        st.markdown('<div class="section-title">Interview Details</div>', unsafe_allow_html=True)
        ty_round = st.radio("Hidden Label", ["Phone Screen", "Technical Interview", "Behavioral Interview", "Final Round / Onsite"], horizontal=True, label_visibility="collapsed", key="ty_round")
        ty_topic = st.text_input("Key topic discussed (optional)", placeholder="e.g. system design, team culture, project X", key="ty_topic")
    elif doc_type == "LinkedIn Message":
        st.markdown('<div class="section-title">LinkedIn Context</div>', unsafe_allow_html=True)
        li_type = st.radio("Hidden Label", ["Connection request to recruiter", "InMail to hiring manager", "Referral request to employee", "Networking message"], horizontal=True, label_visibility="collapsed", key="li_type")

    st.markdown('<div class="section-title">Tone</div>', unsafe_allow_html=True)
    tone = st.select_slider("Hidden Label", ["Very Formal", "Professional", "Friendly & Professional", "Enthusiastic"], value="Professional", label_visibility="collapsed")

    btn_label = {"Cover Letter": "Generate Cover Letter", "Follow-Up Email": "Generate Follow-Up Email", "Thank You Note": "Generate Thank You Note", "LinkedIn Message": "Generate LinkedIn Message", "Cold Outreach Email": "Generate Cold Outreach"}

    if st.button(btn_label.get(doc_type, "Generate"), type="primary", use_container_width=True, disabled=not api_key):
        if not cl_r.strip():
            st.error("Please provide your resume.")
        elif not cl_jd.strip() and doc_type == "Cover Letter":
            st.error("Please paste the job description.")
        else:
            # Build prompt based on doc type
            if doc_type == "Cover Letter":
                doc_prompt = f"""You are an elite career coach writing cover letters that get callbacks at top MNCs. Tone: {tone}.
RESUME: {cl_r}
JOB: {cl_jt or 'the position'} at {cl_co or 'the company'}
HIRING MANAGER: {cl_hm or 'Hiring Manager'}
JD: {cl_jd}
Rules: powerful hook (NOT "I am writing to apply"), 3-4 paragraphs max 380 words, 2-3 specific quantified achievements from resume, 5 ATS keywords naturally, confident call to action. Sound human not generic AI.
Write ONLY the letter starting from "Dear {cl_hm or 'Hiring Manager'}," """
            elif doc_type == "Follow-Up Email":
                doc_prompt = f"""You are an expert at writing follow-up emails that get responses. Tone: {tone}.
RESUME: {cl_r}
JOB: {cl_jt or 'the position'} at {cl_co or 'the company'}
CONTEXT: {fu_context}, it's been {fu_days} days since last contact.
Rules: Subject line first, then email body. Keep under 150 words. Reference specific role/application. Add genuine value (insight about the company/industry). Polite but confident. Include clear next step.
If after rejection: be gracious, express continued interest, ask to be considered for future roles."""
            elif doc_type == "Thank You Note":
                doc_prompt = f"""You are an expert at writing thank-you notes after interviews. Tone: {tone}.
RESUME: {cl_r}
JOB: {cl_jt or 'the position'} at {cl_co or 'the company'}
INTERVIEW ROUND: {ty_round}
KEY TOPIC DISCUSSED: {ty_topic or 'general discussion about the role'}
Rules: Subject line first, then email. Under 200 words. Reference something specific from the conversation. Reinforce your fit with 1 specific example. Express genuine enthusiasm. Send within 24 hours vibe."""
            elif doc_type == "LinkedIn Message":
                doc_prompt = f"""You are a networking expert writing LinkedIn messages that get accepted and replied to. Tone: {tone}.
RESUME: {cl_r}
TARGET: {cl_jt or 'the position'} at {cl_co or 'the company'}
MESSAGE TYPE: {li_type}
Rules: Under 300 characters for connection request, under 500 words for InMail. Be specific about WHY you're reaching out. Mention a genuine commonality. Don't beg or be desperate. Add value first. Make it easy to say yes."""
            else:  # Cold Outreach
                doc_prompt = f"""You are an expert at cold outreach emails that get responses from busy hiring managers. Tone: {tone}.
RESUME: {cl_r}
TARGET: {cl_jt or 'the position'} at {cl_co or 'the company'}
Rules: Catchy subject line. Under 120 words body. Lead with value (what you can do for THEM). One specific impressive achievement with numbers. Easy CTA ("Would a 15-min call work?"). No attachments mention. Sound like a high-performer, not a job beggar."""

            with st.spinner(f"Writing your {doc_type.split(' ', 1)[1]}..."):
                try:
                    letter = ai_call(doc_prompt, temperature=0.75)
                    st.markdown(f'<div class="section-title">Your {doc_type.split(" ", 1)[1]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="resume-output">{letter}</div>', unsafe_allow_html=True)
                    fname = doc_type.split(" ", 1)[1].lower().replace(" ", "_")
                    st.download_button(f"Download {doc_type.split(' ', 1)[1]}", data=letter, file_name=f"{fname}_{(cl_co or 'company').replace(' ','_')}.txt", mime="text/plain", use_container_width=True)
                    st.info("Always personalize the output before sending — add a specific detail about the company or person.")
                except Exception as e:
                    st.error(f"{e}")


# ════════════════════════════════════════════════════════
# INTERVIEW PREP
# ════════════════════════════════════════════════════════
elif page == "Interview Prep":
    st.markdown("""<div class="hero"><div class="hero-badge">Questions · STAR Stories · Salary Negotiation · Difficulty Levels</div>
    <h1>Interview Prep Suite</h1>
    <p>AI-powered interview preparation — questions, STAR story generator, and salary negotiation coaching tailored to YOUR resume</p></div>""", unsafe_allow_html=True)
    if not api_key:
        st.warning("Enter your free API key in the sidebar")

    # ── Mode Selector ──
    ip_mode = st.radio("Hidden Label", ["Interview Questions", "STAR Story Generator", "Salary Negotiation Prep"], horizontal=True, label_visibility="collapsed", key="ip_mode")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="section-title">Your Resume</div>', unsafe_allow_html=True)
        ipt = st.radio("Hidden Label", ["Upload PDF", "Paste Text"], horizontal=True, label_visibility="collapsed", key="ip_rt")
        ip_r = ""
        if ipt == "Upload PDF":
            up = st.file_uploader("Hidden Label", type=["pdf"], label_visibility="collapsed", key="ip_pdf")
            if up:
                try:
                    ip_r = extract_text_from_pdf(up)
                    st.success(f"{len(ip_r.split())} words extracted")
                except ValueError as e:
                    st.error(str(e))
        else:
            ip_r = st.text_area("Hidden Label", height=200, placeholder="Paste resume...", label_visibility="collapsed", key="ip_paste")
    with c2:
        st.markdown('<div class="section-title">Job Details</div>', unsafe_allow_html=True)
        ip_jt = st.text_input("Job Title", placeholder="e.g. Data Engineer", value=st.session_state.get("ip_title", ""), key="ip_jt")
        ip_co = st.text_input("Company", placeholder="e.g. TCS, Google", value=st.session_state.get("ip_company", ""), key="ip_co")
        
        ip_j_mode = st.radio("Provide Job Description:", ["Paste Text", "Scrape URL"], horizontal=True, key="ip_j_mode")
        if ip_j_mode == "Scrape URL":
            ip_url = st.text_input("Job Link URL", placeholder="https://greenhouse.io/...", key="ip_url")
            if ip_url and st.button("Scrape Page", key="ip_scrape"):
                with st.spinner("Extracting..."):
                    scrape_data = fetch_job_description(ip_url)
                    st.session_state["ip_fetched_jd"] = scrape_data["text"]
                    if scrape_data["title"]: st.session_state["ip_title"] = scrape_data["title"]
                    if scrape_data["company"]: st.session_state["ip_company"] = scrape_data["company"]
                    st.rerun()
            ip_jd = st.text_area("Extracted Job Context", value=st.session_state.get("ip_fetched_jd", ""), height=100, key="ip_jd")
        else:
            ip_jd = st.text_area("Job Description", height=140, key="ip_jd_paste", placeholder="Paste job posting here...")

    if ip_mode == "Interview Questions":
        st.markdown('<div class="section-title">Question Settings</div>', unsafe_allow_html=True)
        diff_col, cat_col = st.columns([1, 3])
        with diff_col:
            difficulty = st.radio("**Difficulty**", ["Entry Level", "Mid Level", "Senior Level"], key="ip_diff")
        with cat_col:
            q1, q2, q3, q4 = st.columns(4)
            with q1:
                qt = st.checkbox("Technical", value=True)
            with q2:
                qb = st.checkbox("Behavioral", value=True)
            with q3:
                qs = st.checkbox("Situational", value=True)
            with q4:
                qf = st.checkbox("Company Fit", value=True)
        nq = st.slider("Questions per category", 2, 5, 3)
        if st.button("Generate Interview Questions", type="primary", use_container_width=True, disabled=not api_key):
            if not ip_r.strip():
                st.error("Please provide your resume.")
            elif not ip_jd.strip():
                st.error("Please paste the job description.")
            else:
                diff_text = difficulty.split(" ", 1)[1]
                types = [t for t, c in [("Technical (role-specific skills, tools, concepts)", qt), ("Behavioral (STAR format, past experiences)", qb), ("Situational (hypothetical scenarios)", qs), ("Company Fit (culture, motivation, goals)", qf)] if c]
                with st.spinner("Generating your personalized interview guide..."):
                    try:
                        guide = ai_call(f"""You are a senior interviewer at a top MNC with 15 years hiring for {ip_jt or 'tech'} roles.
DIFFICULTY LEVEL: {diff_text} — adjust question complexity accordingly.
RESUME: {ip_r}
ROLE: {ip_jt or 'the role'} at {ip_co or 'top MNC'}
JD: {ip_jd}
Generate {nq} questions for EACH: {', '.join(types)}
For EVERY question: Question (specific to their resume, calibrated for {diff_text} level), Why asked (1 sentence), Ideal answer (3-4 bullets using their actual experience), Common mistake to avoid, Follow-up question the interviewer might ask.
Reference actual projects/skills from THEIR resume. Format with clear headers and emojis.""", temperature=0.6)
                        st.markdown('<div class="section-title">Your Interview Prep Guide</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="resume-output">{guide}</div>', unsafe_allow_html=True)
                        st.download_button("Download Interview Guide", data=guide, file_name=f"interview_{(ip_jt or 'prep').replace(' ', '_')}.txt", mime="text/plain", use_container_width=True)
                        st.info("Practice each answer out loud 3 times. Record yourself — it works!")
                    except Exception as e:
                        st.error(f"{e}")

    elif ip_mode == "STAR Story Generator":
        st.markdown("""<div class="info-box"><strong>STAR Method:</strong> Situation → Task → Action → Result. This generator creates polished STAR stories from your actual resume experiences — ready to use in behavioral interviews.</div>""", unsafe_allow_html=True)
        star_count = st.slider("Number of STAR stories to generate", 3, 8, 5, key="star_count")
        if st.button("Generate STAR Stories", type="primary", use_container_width=True, disabled=not api_key):
            if not ip_r.strip():
                st.error("Please provide your resume.")
            else:
                with st.spinner("Crafting your STAR stories..."):
                    try:
                        stars = ai_call(f"""You are a career coach who specializes in behavioral interview preparation using the STAR method.

RESUME: {ip_r}
TARGET ROLE: {ip_jt or 'tech role'} at {ip_co or 'top company'}
JD: {ip_jd or 'general tech role'}

Generate {star_count} polished STAR stories based on REAL experiences from this resume.

For EACH story:
STORY TITLE (e.g. "Led Database Migration Under Tight Deadline")
BEST FOR: (which interview question types this answers — e.g. leadership, problem-solving, teamwork)

SITUATION: Set the scene (2-3 sentences, specific company/project from resume)
TASK: What was your specific responsibility (1-2 sentences)
ACTION: What you specifically did — step by step (3-4 bullets with technical details)
RESULT: Quantified outcome with numbers/percentages (2-3 bullets)

POWER PHRASES TO USE: 3 impressive phrases to drop naturally during the telling

Pick diverse experiences covering: leadership, technical challenge, teamwork, failure/recovery, and initiative.
Make stories feel authentic and conversational, not robotic.""", temperature=0.6, max_tokens=3000)
                        st.markdown('<div class="section-title">Your STAR Stories</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="resume-output">{stars}</div>', unsafe_allow_html=True)
                        st.download_button("Download STAR Stories", data=stars, file_name="star_stories.txt", mime="text/plain", use_container_width=True)
                        st.info("Memorize these stories loosely — don't recite them word-for-word. Practice telling each one in under 2 minutes.")
                    except Exception as e:
                        st.error(f"{e}")

    elif ip_mode == "Salary Negotiation Prep":
        st.markdown("""<div class="info-box"><strong>Salary Negotiation:</strong> AI will analyze your resume, the target role, and current market data to create a personalized negotiation strategy with scripts you can use word-for-word.</div>""", unsafe_allow_html=True)
        sal_col1, sal_col2 = st.columns(2)
        with sal_col1:
            current_sal = st.text_input("Current/Last Salary (optional)", placeholder="e.g. $85,000 or ₹12 LPA", key="cur_sal")
        with sal_col2:
            target_sal = st.text_input("Target Salary (optional)", placeholder="e.g. $120,000 or ₹18 LPA", key="tgt_sal")
        if st.button("Generate Negotiation Strategy", type="primary", use_container_width=True, disabled=not api_key):
            if not ip_r.strip():
                st.error("Please provide your resume.")
            else:
                with st.spinner("Building your negotiation strategy..."):
                    try:
                        neg = ai_call(f"""You are a salary negotiation expert who has coached 1000+ tech professionals to get 20-40% higher offers.

RESUME: {ip_r}
TARGET ROLE: {ip_jt or 'tech role'} at {ip_co or 'a company'}
JD: {ip_jd or 'general tech role'}
CURRENT SALARY: {current_sal or 'not disclosed'}
TARGET SALARY: {target_sal or 'market rate'}

Provide a COMPLETE negotiation strategy:

1. MARKET ANALYSIS
   - Estimated salary range for this role (low / mid / high / top)
   - How this candidate's experience positions them in that range
   - Factors that increase/decrease their leverage

2. YOUR ANCHOR NUMBER
   - Specific number to ask for first and WHY
   - Your walk-away minimum

3. NEGOTIATION SCRIPTS (word-for-word)
   - When asked "What are your salary expectations?"
   - When they give a low offer
   - When they say "That's above our budget"
   - When asking for more equity/RSUs/bonus instead
   - When negotiating PTO, remote work, signing bonus

4. LEVERAGE POINTS from their resume (specific achievements to reference)

5. MISTAKES TO AVOID

6. TIMING: When to negotiate (which stage of the process)

Be specific with numbers. Use the resume's actual achievements as leverage.""", temperature=0.5, max_tokens=2500)
                        st.markdown('<div class="section-title">Your Negotiation Strategy</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="resume-output">{neg}</div>', unsafe_allow_html=True)
                        st.download_button("Download Negotiation Strategy", data=neg, file_name="salary_negotiation.txt", mime="text/plain", use_container_width=True)
                        st.info("Never give your number first. Always let them make the first offer, then negotiate up using these scripts.")
                    except Exception as e:
                        st.error(f"{e}")


# ════════════════════════════════════════════════════════
# RESUME BUILDER
# ════════════════════════════════════════════════════════
elif page == "Resume Builder":
    st.markdown("""<div class="hero"><div class="hero-badge">Build Fresh · Rewrite for Job · LinkedIn Optimizer · 100% ATS</div>
    <h1>AI Resume & LinkedIn Builder</h1>
    <p>Build a perfect resume from scratch, rewrite for any job, or optimize your LinkedIn profile — all AI-powered</p></div>""", unsafe_allow_html=True)
    if not api_key:
        st.warning("Enter your free API key in the sidebar")

    mode = st.radio("Hidden Label", ["Build Fresh Resume", "Rewrite for New Job", "LinkedIn Profile Optimizer"], horizontal=True, label_visibility="collapsed", key="rb_mode")
    st.markdown("---")

    # ── MODE: REWRITE ──
    if mode == "Rewrite for New Job":
        st.markdown("""<div class="info-box"><strong>How this works:</strong> Paste your current resume → paste the target job description
        → AI completely rewrites your resume to be 100% ATS-optimized for that specific job.
        Your facts stay accurate, but language, keywords, and structure are rebuilt for maximum impact.</div>""", unsafe_allow_html=True)

        rw1, rw2 = st.columns(2, gap="large")
        with rw1:
            st.markdown('<div class="section-title">Your Current Resume</div>', unsafe_allow_html=True)
            rwt = st.radio("Hidden Label", ["Upload PDF", "Paste Text"], horizontal=True, label_visibility="collapsed", key="rw_rt")
            rw_cur = ""
            if rwt == "Upload PDF":
                up = st.file_uploader("Hidden Label", type=["pdf"], label_visibility="collapsed", key="rw_pdf")
                if up:
                    try:
                        rw_cur = extract_text_from_pdf(up)
                        st.success(f"Extracted {len(rw_cur.split())} words from **{up.name}**")
                        with st.expander("Preview extracted text"):
                            st.text(rw_cur[:600] + "..."if len(rw_cur) > 600 else rw_cur)
                    except ValueError as e:
                        st.error(str(e))
            else:
                rw_cur = st.text_area("Hidden Label", height=300, placeholder="Paste your complete current resume here...", label_visibility="collapsed", key="rw_paste")
        with rw2:
            st.markdown('<div class="section-title">Target Job</div>', unsafe_allow_html=True)
            rw_jt = st.text_input("Job Title *", placeholder="e.g. Data Engineer, AI Engineer", value=st.session_state.get("rw_title", ""), key="rw_jt")
            rw_co = st.text_input("Company (optional)", placeholder="e.g. Google, Amazon, TCS", value=st.session_state.get("rw_company", ""), key="rw_co")
            
            rw_j_mode = st.radio("Provide Job Description:", ["Paste Text", "Scrape URL"], horizontal=True, key="rw_j_mode")
            if rw_j_mode == "Scrape URL":
                rw_url = st.text_input("Job Link URL", placeholder="https://greenhouse.io/...", key="rw_url")
                if rw_url and st.button("Scrape Page", key="rw_scrape"):
                    with st.spinner("Extracting..."):
                        scrape_data = fetch_job_description(rw_url)
                        st.session_state["rw_fetched_jd"] = scrape_data["text"]
                        if scrape_data["title"]: st.session_state["rw_title"] = scrape_data["title"]
                        if scrape_data["company"]: st.session_state["rw_company"] = scrape_data["company"]
                        st.rerun()
                rw_jd = st.text_area("Extracted Job Context", value=st.session_state.get("rw_fetched_jd", ""), height=120, key="rw_jd")
            else:
                rw_jd = st.text_area("Job Description *", height=220, placeholder="Paste the full job posting here — the more detail, the better the rewrite...", key="rw_jd_paste")

        st.markdown('<div class="section-title">Rewrite Options</div>', unsafe_allow_html=True)
        op1, op2, op3 = st.columns(3)
        with op1:
            rw_ats = st.checkbox("Aggressive ATS keywords", value=True, help="Heavily injects job keywords throughout")
        with op2:
            rw_num = st.checkbox("Add estimated metrics", value=True, help="AI adds realistic numbers/% where missing")
        with op3:
            rw_lang = st.checkbox("Modernize language", value=True, help="Replace weak verbs with power action words")

        if st.button("Rewrite My Resume", type="primary", use_container_width=True, disabled=not api_key):
            if not rw_cur.strip():
                st.error("Please provide your current resume.")
            elif not rw_jd.strip():
                st.error("Please paste the target job description.")
            elif len(rw_jd) < 50:
                st.error("Job description too short — paste the full posting.")
            else:
                ats_rule = "Inject EXACT keywords from JD throughout every section. Mirror job description language precisely. Front-load each bullet with the most important keyword."if rw_ats else "Naturally weave in relevant keywords."
                num_rule = "Add realistic quantified achievements where missing (e.g. 'reduced processing time by 40%', 'managed 3+ projects simultaneously'). Every bullet needs at least one number or % or scale."if rw_num else "Keep existing metrics."
                lang_rule = "Replace ALL weak verbs (helped, worked, assisted) with power verbs (Engineered, Architected, Spearheaded, Automated, Optimized). Remove all filler phrases like 'responsible for'."if rw_lang else "Improve language where clearly weak."
                prompt = f"""You are the world's best resume writer specializing in ATS optimization for top MNC companies.
TASK: Completely rewrite this resume to achieve 95%+ ATS score for this specific job.

CURRENT RESUME:
{rw_cur}

TARGET JOB: {rw_jt or 'the role'} at {rw_co or 'the company'}
JOB DESCRIPTION:
{rw_jd}

REWRITE RULES:
- {ats_rule}
- {num_rule}
- {lang_rule}
- Keep ALL facts 100% accurate (companies, dates, education, certifications — never fabricate)
- Structure: Contact → Professional Summary → Key Achievements → Experience → Skills → Projects → Education → Certifications
- Professional Summary: 3 powerful sentences — target job title + top 3 matching skills + unique value
- Skills: organized by category, job-critical skills listed FIRST
- Each bullet: [Power Verb] + [What you did] + [Tool/Tech] + [Measurable result]
- Add a "Key Achievements"callout with 3 most impressive accomplishments
- Keep to 1-2 pages of content (700-900 words)

Output the COMPLETE rewritten resume, ready to copy-paste. Start with the person's name as header."""
                with st.spinner(f"Rewriting your resume for **{rw_jt or 'the role'}**... (~20 seconds)"):
                    try:
                        rewritten = ai_call(prompt, temperature=0.35, max_tokens=3000)
                        st.markdown("---")
                        st.markdown("""<div class="success-box"><strong>Resume rewritten!</strong>
                        Your resume is now ATS-optimized for this specific job.
                        Go to <strong>Analyzer</strong> tab to verify your ATS score — aim for 80%+!</div>""", unsafe_allow_html=True)
                        st.markdown('<div class="section-title">Your Rewritten Resume</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="resume-output">{rewritten}</div>', unsafe_allow_html=True)
                        d1, d2 = st.columns(2)
                        with d1:
                            st.download_button("Download Rewritten Resume", data=rewritten, file_name=f"resume_{(rw_jt or 'rewritten').replace(' ', '_')}.txt", mime="text/plain", use_container_width=True)
                        with d2:
                            st.download_button("Download Both Versions", data=f"ORIGINAL:\n{'='*50}\n{rw_cur}\n\nREWRITTEN:\n{'='*50}\n{rewritten}", file_name="resume_comparison.txt", mime="text/plain", use_container_width=True)
                        st.markdown("""<div class="win-box"><strong>Next Steps:</strong><br>
                        1. Copy the resume above → paste into Google Docs → format cleanly<br>
                        2. Go to <strong>Analyzer</strong> → paste this resume + job description → check ATS score<br>
                        3. Aim for 80%+ before applying. Rewrite again if needed!</div>""", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"{e}")

    # ── MODE: BUILD FRESH ──
    elif mode == "Build Fresh Resume":
        st.markdown("""<div class="info-box"><strong>How this works:</strong> Fill in your details → AI builds a complete,
        professional, ATS-optimized resume tailored to your target job. Takes about 20 seconds.</div>""", unsafe_allow_html=True)
        st.markdown('<div class="section-title">Personal Info</div>', unsafe_allow_html=True)
        p1, p2 = st.columns(2, gap="large")
        with p1:
            rb_name = st.text_input("Full Name *", placeholder="Yagyesh Vyas", key="rb_name")
            rb_mail = st.text_input("Email *", placeholder="you@gmail.com", key="rb_mail")
            rb_ph = st.text_input("Phone", placeholder="+1 (123) 456-7890", key="rb_ph")
            rb_loc = st.text_input("Location", placeholder="Richmond, VA, USA", key="rb_loc")
        with p2:
            rb_tgt = st.text_input("Target Job Title *", placeholder="e.g. Data Engineer, AI Engineer", value=st.session_state.get("rb2_title", ""), key="rb_tgt")
            rb_li = st.text_input("LinkedIn URL", placeholder="linkedin.com/in/yourname", key="rb_li")
            rb_gh = st.text_input("GitHub URL", placeholder="github.com/yourname", key="rb_gh")
            rb_port = st.text_input("Portfolio URL", placeholder="yoursite.com", key="rb_port")
        st.markdown('<div class="section-title">Education</div>', unsafe_allow_html=True)
        rb_edu = st.text_area("Hidden Label", height=85, label_visibility="collapsed", key="rb_edu",
                              placeholder="Master's in CS, University of the Potomac, 2024–2026, GPA 3.88\nBachelor's in CS, GTU, 2019–2022, GPA 8.08")
        st.markdown('<div class="section-title">Work Experience</div>', unsafe_allow_html=True)
        rb_exp = st.text_area("Hidden Label", height=120, label_visibility="collapsed", key="rb_exp",
                              placeholder="Data & IT Developer Intern, MKL Management LLC, Feb 2025–Oct 2025\n- Built Python automation scripts\n- Designed Power BI dashboards\n- Managed SQL databases")
        st.markdown('<div class="section-title">Skills & Projects</div>', unsafe_allow_html=True)
        sk1, sk2 = st.columns(2, gap="large")
        with sk1:
            rb_sk = st.text_area("Technical Skills (comma-separated)", height=85, key="rb_sk", placeholder="Python, SQL, Power BI, Docker, AWS, Streamlit, REST APIs, Git...")
        with sk2:
            rb_pr = st.text_area("Projects", height=85, key="rb_pr", placeholder="AI Career Suite — Python, OpenRouter API, Streamlit. Live at streamlit.app")
        st.markdown('<div class="section-title">Certifications & Target JD</div>', unsafe_allow_html=True)
        ce1, ce2 = st.columns(2, gap="large")
        with ce1:
            rb_cert = st.text_area("Certifications", height=75, key="rb_cert", placeholder="AWS ML Fundamentals, Jan 2026\nKubernetes Cloud Native, Jan 2026")
        with ce2:
            rb_j_mode = st.radio("Provide Target JD:", ["Paste Text", "Scrape URL"], horizontal=True, key="rb2_j_mode")
            if rb_j_mode == "Scrape URL":
                rb2_url = st.text_input("Job Link URL", placeholder="https://greenhouse.io/...", key="rb2_url")
                if rb2_url and st.button("Scrape Page", key="rb2_scrape"):
                    with st.spinner("Extracting..."):
                        scrape_data = fetch_job_description(rb2_url)
                        st.session_state["rb2_fetched_jd"] = scrape_data["text"]
                        if scrape_data["title"]: st.session_state["rb2_title"] = scrape_data["title"]
                        st.rerun()
                rb_jd = st.text_area("Extracted Job Context", value=st.session_state.get("rb2_fetched_jd", ""), height=75, key="rb_jd2")
            else:
                rb_jd = st.text_area("Target Job Description (recommended)", height=75, key="rb_jd2_paste", placeholder="Paste the job you're targeting for a tailored resume...")

        if st.button("Build My Resume", type="primary", use_container_width=True, disabled=not api_key):
            if not rb_name.strip() or not rb_mail.strip() or not rb_tgt.strip():
                st.error("Please fill in Name, Email, and Target Job Title.")
            else:
                with st.spinner("Building your ATS-optimized resume..."):
                    try:
                        output = ai_call(f"""You are the world's best resume writer. Build a complete ATS-optimized resume.
Name:{rb_name} | Email:{rb_mail} | Phone:{rb_ph} | Location:{rb_loc}
LinkedIn:{rb_li} | GitHub:{rb_gh} | Portfolio:{rb_port} | Target:{rb_tgt}
EDUCATION: {rb_edu}
EXPERIENCE: {rb_exp}
SKILLS: {rb_sk}
PROJECTS: {rb_pr}
CERTIFICATIONS: {rb_cert}
TARGET JD: {rb_jd or f'General {rb_tgt} role'}

Rules: Professional Summary (3 sentences, target title+top skills+value), power verbs+quantified results, skills by category, ATS keywords from JD throughout, clear section headers with === markers, 600-800 words. Output COMPLETE copy-paste-ready resume.""", temperature=0.35, max_tokens=3000)
                        st.markdown("---")
                        st.markdown('<div class="success-box"><strong>Resume built!</strong> Now go to <strong>Analyzer</strong> tab to check your ATS score!</div>', unsafe_allow_html=True)
                        st.markdown('<div class="section-title">Your AI-Built Resume</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="resume-output">{output}</div>', unsafe_allow_html=True)
                        st.download_button("Download Resume", data=output, file_name=f"resume_{rb_name.replace(' ', '_')}.txt", mime="text/plain", use_container_width=True)
                        st.info("Copy into Google Docs → format cleanly → go to Analyzer to verify ATS score!")
                    except Exception as e:
                        st.error(f"{e}")

    # ── MODE: LINKEDIN OPTIMIZER ──
    elif mode == "LinkedIn Profile Optimizer":
        st.markdown("""<div class="info-box"><strong>LinkedIn Optimizer:</strong> Paste your current LinkedIn profile (or resume) and target role — AI will generate an optimized LinkedIn Headline, About section, Experience bullets, and Featured section suggestions.</div>""", unsafe_allow_html=True)

        li1, li2 = st.columns(2, gap="large")
        with li1:
            st.markdown('<div class="section-title">Your Resume / LinkedIn Profile</div>', unsafe_allow_html=True)
            li_input_type = st.radio("Hidden Label", ["Upload PDF", "Paste Text"], horizontal=True, label_visibility="collapsed", key="li_rt")
            li_text = ""
            if li_input_type == "Upload PDF":
                up = st.file_uploader("Hidden Label", type=["pdf"], label_visibility="collapsed", key="li_pdf")
                if up:
                    try:
                        li_text = extract_text_from_pdf(up)
                        st.success(f"{len(li_text.split())} words extracted")
                    except ValueError as e:
                        st.error(str(e))
            else:
                li_text = st.text_area("Hidden Label", height=250, placeholder="Paste your resume or current LinkedIn profile text...", label_visibility="collapsed", key="li_paste")
        with li2:
            st.markdown('<div class="section-title">Target Role</div>', unsafe_allow_html=True)
            li_role = st.text_input("Target Job Title", placeholder="e.g. Senior Data Engineer", key="li_role")
            li_industry = st.text_input("Industry", placeholder="e.g. FinTech, HealthTech, FAANG", key="li_industry")
            li_jd = st.text_area("Target JD (optional but recommended)", height=140, placeholder="Paste a job description to tailor your LinkedIn for...", key="li_jd")

        st.markdown('<div class="section-title">Optimize</div>', unsafe_allow_html=True)
        lo1, lo2, lo3, lo4 = st.columns(4)
        with lo1:
            lo_headline = st.checkbox("Headline", value=True)
        with lo2:
            lo_about = st.checkbox("About Section", value=True)
        with lo3:
            lo_exp = st.checkbox("Experience Bullets", value=True)
        with lo4:
            lo_featured = st.checkbox("Featured Suggestions", value=True)

        if st.button("Optimize My LinkedIn", type="primary", use_container_width=True, disabled=not api_key):
            if not li_text.strip():
                st.error("Please provide your resume or LinkedIn profile.")
            elif not li_role.strip():
                st.error("Please enter your target job title.")
            else:
                sections = [s for s, c in [("HEADLINE (120 char max, keyword-rich, attention-grabbing)", lo_headline), ("ABOUT SECTION (2600 char max, 3 paragraphs: hook + achievements + CTA)", lo_about), ("EXPERIENCE BULLETS (rewrite top 3 roles with LinkedIn-optimized bullets — longer than resume, more storytelling)", lo_exp), ("FEATURED SECTION (3-5 suggestions for what to feature: projects, certifications, published articles, posts)", lo_featured)] if c]
                with st.spinner("Optimizing your LinkedIn profile..."):
                    try:
                        linkedin = ai_call(f"""You are a LinkedIn optimization expert who has helped 500+ professionals get 10x more recruiter views.

RESUME/PROFILE: {li_text}
TARGET ROLE: {li_role}
INDUSTRY: {li_industry or 'Tech'}
TARGET JD: {li_jd or f'General {li_role} position'}

Optimize these sections:
{chr(10).join(f'- {s}'for s in sections)}

Rules:
- Use keywords recruiters search for in this industry
- Headline: [Title] | [Key Skill 1] | [Key Skill 2] | [Unique Value] — NO emojis in headline
- About: Start with a powerful hook question or stat. Use first person. Include 3 quantified achievements. End with what you're looking for and how to reach you. Use line breaks and emojis sparingly.
- Experience: Each bullet should be 2-3 lines (LinkedIn allows more than resumes). Add context, tools, and results.
- Featured: Suggest specific types of content with examples
- Add a KEYWORDS section at the end: 20 recruiter search terms this profile should rank for

Make it sound human, confident, and authentic — not like generic AI.""", temperature=0.5, max_tokens=2500)
                        st.markdown('<div class="section-title">Your Optimized LinkedIn Profile</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="resume-output">{linkedin}</div>', unsafe_allow_html=True)
                        st.download_button("Download LinkedIn Optimization", data=linkedin, file_name="linkedin_optimized.txt", mime="text/plain", use_container_width=True)
                        st.markdown("""<div class="win-box"><strong>Next Steps:</strong><br>
                        1. Update your LinkedIn headline first (most impactful change)<br>
                        2. Rewrite your About section<br>
                        3. Update your 3 most recent Experience entries<br>
                        4. Add Featured items<br>
                        5. Turn on "Open to Work"badge (visible to recruiters only)</div>""", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"{e}")


# ════════════════════════════════════════════════════════
# DASHBOARD
# ════════════════════════════════════════════════════════
elif page == "Dashboard":
    st.markdown("""<div class="hero"><div class="hero-badge">Progress · Trends · Insights · Career Intelligence</div>
    <h1>Career Analytics Dashboard</h1>
    <p>Track your resume improvements, identify skill gaps, and get AI-powered career intelligence</p></div>""", unsafe_allow_html=True)
    analyses = get_all_analyses()
    ms = get_top_missing_skills()
    st_data = get_score_trend()
    if not analyses:
        st.info("No analyses yet. Go to **Analyzer** to get started!")
    else:
        avg_ats = sum(a["ats_score"] for a in analyses) / len(analyses)
        avg_m = sum(a["match_score"] for a in analyses) / len(analyses)
        best = max(a["ats_score"] for a in analyses)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Analyses", len(analyses))
        m2.metric("Avg ATS", f"{avg_ats:.0f}/100")
        m3.metric("Avg Match", f"{avg_m:.0f}/100")
        m4.metric("Best ATS", f"{best}/100")
        if len(st_data) >= 2:
            st.markdown('<div class="section-title">Score Improvement Over Time</div>', unsafe_allow_html=True)
            df = pd.DataFrame(st_data)
            fig_line = px.area(df, x="date", y=["ats", "match"], 
                               labels={"value": "Score (0-100)", "date": "Date"},
                               color_discrete_sequence=["#8b5cf6", "#10b981"])
            fig_line.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#94a3b8"), legend_title_text="Metric", margin=dict(l=0, r=0, t=10, b=0))
            st.plotly_chart(fig_line, use_container_width=True)
            
        if ms:
            st.markdown('<div class="section-title">Skills You Keep Missing — Learn These First</div>', unsafe_allow_html=True)
            df2 = pd.DataFrame(ms).head(8)
            
            # Create a futuristic Radar Chart for missing skills
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=df2["times_missing"].tolist(),
                theta=df2["skill"].tolist(),
                fill='toself',
                name='Missing Frequency',
                line_color='#ec4899',
                fillcolor='rgba(236,72,153,0.3)'
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, df2["times_missing"].max() + 1]), bgcolor="rgba(0,0,0,0)"),
                showlegend=False,
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e2e8f0"), margin=dict(l=40, r=40, t=20, b=20)
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('<div class="section-title">Analysis History</div>', unsafe_allow_html=True)
        for a in analyses:
            icon = ""if a["ats_score"] >= 70 else (""if a["ats_score"] >= 50 else "")
            with st.expander(f"{icon} {a['job_title'] or 'Unknown'}{'@ '+a['company_name'] if a['company_name'] else ''} — ATS {a['ats_score']} · Match {a['match_score']} · {a['created_at'][:10]}"):
                h1, h2 = st.columns(2)
                with h1:
                    st.markdown("**Matched:**")
                    st.markdown(chips(a["matched_skills"][:8], "chip-green"), unsafe_allow_html=True)
                with h2:
                    st.markdown("**Missing:**")
                    st.markdown(chips(a["missing_skills"][:8], "chip-red"), unsafe_allow_html=True)
                st.markdown(f"**Summary:** {a['overall_summary']}")
                if st.button("Delete", key=f"del_{a['id']}"):
                    delete_analysis(a["id"])
                    st.rerun()

        # ── AI CAREER COACH ──
        st.markdown('---')
        st.markdown('<div class="section-title">AI Career Coach — Personalized Roadmap</div>', unsafe_allow_html=True)
        st.markdown("""<div class="info-box"><strong>Based on your analysis history:</strong> AI will analyze ALL your past results to create a personalized learning roadmap, identify career patterns, and suggest your best next moves.</div>""", unsafe_allow_html=True)

        coach1, coach2 = st.columns(2)
        with coach1:
            if st.button("Generate Learning Roadmap", use_container_width=True, disabled=not api_key, key="coach_road"):
                # Gather all skill data
                all_missing = []
                all_matched = []
                jobs_analyzed = []
                for a in analyses:
                    all_missing.extend(a.get("missing_skills", []))
                    all_matched.extend(a.get("matched_skills", []))
                    jobs_analyzed.append(f"{a.get('job_title','Unknown')} @ {a.get('company_name','')}")

                with st.spinner("Building your personalized learning roadmap..."):
                    try:
                        roadmap = ai_call(f"""You are a senior career coach. Based on this person's job search data, create a PERSONALIZED LEARNING ROADMAP.

JOBS ANALYZED: {', '.join(jobs_analyzed[:10])}
SKILLS THEY HAVE: {', '.join(set(all_matched))}
SKILLS THEY KEEP MISSING: {', '.join(set(all_missing))}
AVERAGE ATS SCORE: {avg_ats:.0f}/100
TOTAL ANALYSES: {len(analyses)}

Create:
1. TOP 5 SKILLS TO LEARN (ordered by impact on their job search — which skills appear most in their missing list)
2. LEARNING PLAN (for each skill: best free resource, estimated time, hands-on project idea)
3. 30-DAY ACTION PLAN (week by week, specific daily actions)
4. QUICK WINS (3 skills they can learn in under a weekend that most jobs want)
5. CAREER PATTERN ANALYSIS (based on the jobs they're applying to — are they focused or scattered? advice on strategy)
6. IDEAL TARGET (based on their existing skills, what role title should they focus on for best match?)

Be specific with resource links (Coursera, YouTube, free courses). Make it actionable, not generic.""", temperature=0.5, max_tokens=2500)
                        st.markdown(f'<div class="resume-output">{roadmap}</div>', unsafe_allow_html=True)
                        st.download_button("Download Learning Roadmap", data=roadmap, file_name="learning_roadmap.txt", mime="text/plain", use_container_width=True, key="dl_roadmap")
                    except Exception as e:
                        st.error(f"{e}")

        with coach2:
            # Export all data
            if st.button("Export All Data", use_container_width=True, key="export_all"):
                export_lines = ["AI CAREER SUITE — COMPLETE ANALYSIS EXPORT", "="* 60, ""]
                for a in analyses:
                    export_lines.append(f"Job: {a.get('job_title','N/A')} @ {a.get('company_name','N/A')}")
                    export_lines.append(f"Date: {a.get('created_at','N/A')}")
                    export_lines.append(f"ATS: {a['ats_score']}/100 | Match: {a['match_score']}/100")
                    export_lines.append(f"Matched: {', '.join(a.get('matched_skills',[]))}")
                    export_lines.append(f"Missing: {', '.join(a.get('missing_skills',[]))}")
                    export_lines.append(f"Summary: {a.get('overall_summary','N/A')}")
                    export_lines.append("-"* 40)
                    export_lines.append("")
                export_text = "\n".join(export_lines)
                st.download_button("Download Export File", data=export_text, file_name="career_suite_export.txt", mime="text/plain", use_container_width=True, key="dl_export")


# ════════════════════════════════════════════════════════
# JOB DISCOVERY
# ════════════════════════════════════════════════════════
elif page == "Job Discovery":
    st.markdown("""<div class="hero"><div class="hero-badge">Smart Search · Portfolio matching · Market Data</div>
    <h1>Job Discovery Engine</h1>
    <p>Upload your resume and let AI find the best roles, companies, and direct search links for you instantly.</p></div>""", unsafe_allow_html=True)
    
    jd_r_type = st.radio("Resume Source:", ["Upload PDF", "Paste Text"], horizontal=True, key="jd_r_type")
    jd_resume = ""
    if jd_r_type == "Upload PDF":
        up = st.file_uploader("Hidden Label", type=["pdf"], label_visibility="collapsed", key="jd_pdf")
        if up: jd_resume = extract_text_from_pdf(up)
    else:
        jd_resume = st.text_area("Paste Resume", height=200, key="jd_paste")

    st.markdown('<div class="section-title">Location (Optional)</div>', unsafe_allow_html=True)
    jd_loc = st.text_input("Hidden Label", placeholder="e.g. Remote, New York, Bangalore", key="jd_loc", label_visibility="collapsed")

    if st.button("Discover My Next Role", type="primary", use_container_width=True, disabled=not api_key):
        if not jd_resume.strip():
            st.error("Please provide your resume first.")
        else:
            with st.spinner("Scanning global job markets and analyzing your fit..."):
                try:
                    discovery = ai_call(f"""You are a career growth strategist. Analyze this resume and help the user find jobs.
                    
RESUME: {jd_resume}
LOCATION PREFERENCE: {jd_loc or 'Global/Remote'}

Provide:
1. RECOMMENDED ROLES: Top 3 job titles they should hunt for (most qualified).
2. TARGET COMPANIES: 5 specific companies (MNC + Startups) that hire for these roles and would value this background.
3. SMART SEARCH STRATEGY: One sentence on how to filter results for maximum success.
4. DIRECT SEARCH LINKS: For EACH recommended role, provide a direct clickable URL for:
   - LinkedIn Jobs: https://www.linkedin.com/jobs/search/?keywords=[ROLENAME_URL_ENCODED]&location=[LOCATION_URL_ENCODED]
   - Indeed Jobs: https://www.indeed.com/jobs?q=[ROLENAME_URL_ENCODED]&l=[LOCATION_URL_ENCODED]
   - Google Jobs: https://www.google.com/search?q=jobs+near+me+[ROLENAME_URL_ENCODED]
5. MARKET SALARY: Estimated range for these roles based on the experience level in resume.
6. THE "HIDDEN"PATH: One alternative career path where these skills transition perfectly.

Format with beautiful markdown, bold headers, and emojis. Ensure URLs are properly formatted as markdown [Label](URL).""", temperature=0.6, max_tokens=2000)
                    
                    st.markdown('<div class="section-title">Your Career Roadmap</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="resume-output">{discovery}</div>', unsafe_allow_html=True)
                    
                    # Also suggest a copilot follow-up
                    st.info("Pro Tip: Copy one of these roles and head to the **AI Copilot** to practice a mock interview for it!")
                    
                except Exception as e:
                    st.error(f"{e}")
# ════════════════════════════════════════════════════════
# AI COPILOT
# ════════════════════════════════════════════════════════
elif page == "AI Copilot":
    st.markdown("""<div class="hero"><div class="hero-badge">Interactive · Conversational · Always On</div>
    <h1>AI Career Copilot</h1>
    <p>Chat directly with your AI coach. Ask it to rewrite a specific bullet, conduct a mock interview, or give salary advice.</p></div>""", unsafe_allow_html=True)
    
    if "messages"not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! I am your AI Career Copilot. You can set your resume and job description via the 'Set Context'menu above. How can I help you today? (e.g. 'Rewrite my 3rd bullet point', 'Roleplay an Amazon interview with me', 'Help me find a job')"}]

    if not api_key:
        st.warning("Please provide an API key in the sidebar to chat with the Copilot.")
    else:
        with st.expander("Set Context (Optional: Provide your Resume & Job Description)", expanded=False):
            c1, c2 = st.columns(2)
            with c1:
                cp_r_type = st.radio("Resume Input:", ["Paste Text", "Upload PDF"], horizontal=True, key="cp_r_type")
                copilot_r = ""
                if cp_r_type == "Upload PDF":
                    up = st.file_uploader("Hidden Label", type=["pdf"], label_visibility="collapsed", key="cp_pdf")
                    if up:
                        copilot_r = extract_text_from_pdf(up)
                else:
                    copilot_r = st.text_area("Resume Content", height=150, key="cp_r", placeholder="Paste your resume here...")
            with c2:
                cp_j_mode = st.radio("Provide Job Description:", ["Paste Text", "Scrape URL"], horizontal=True, key="cp_j_mode")
                if cp_j_mode == "Scrape URL":
                    cp_url = st.text_input("Job Link URL", placeholder="https://greenhouse.io/...", key="cp_url")
                    if cp_url and st.button("Scrape Page", key="cp_scrape"):
                        with st.spinner("Extracting..."):
                            scrape_data = fetch_job_description(cp_url)
                            st.session_state["cp_fetched_jd"] = scrape_data["text"]
                            st.rerun()
                    copilot_jd = st.text_area("Extracted Job Context", value=st.session_state.get("cp_fetched_jd", ""), height=100, key="cp_jd")
                else:
                    copilot_jd = st.text_area("Job Description", height=150, key="cp_jd_paste", placeholder="Paste job posting here...")

        # Display chat messages
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Chat input
        if prompt := st.chat_input("Ask your career coach anything..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Build Context
            context = ""
            if copilot_r or copilot_jd:
                context += "\n[User's Provided Context]\n"
                if copilot_r:
                    context += f"RESUME:\n{copilot_r}\n\n"
                if copilot_jd:
                    context += f"TARGET JOB:\n{copilot_jd}\n\n"
            elif "last_result"in st.session_state:
                lr = st.session_state["last_result"]
                context += f"\n[Previous Analysis Context: The user applied for '{lr.get('job_title', 'a job')}'at '{lr.get('company_name', 'a company')}'. ATS Score: {lr.get('ats_score', 0)}.]\n\n"

            # Prepare messages for API
            system_prompt = "You are an elite executive career coach and technical recruiter. "+ context + "Help the user negotiate salary, rewrite resume points, practice interviews, or suggest how to find a job. Keep responses highly actionable and concise."
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        # Construct prompt history
                        history = "\\n".join([f"{m['role'].capitalize()}: {m['content']}"for m in st.session_state.messages[-5:]])
                        full_prompt = f"{system_prompt}\\n\\nConversation History:\\n{history}\\n\\nAssistant:"
                        
                        response = ai_call(full_prompt, temperature=0.6, max_tokens=1000)
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        st.error(f"Error: {e}")


# ════════════════════════════════════════════════════════
# API GUIDE
# ════════════════════════════════════════════════════════
elif page == "API Guide":
    st.markdown("""<div class="hero">
        <div class="hero-badge">Free · Paid · Step-by-Step Setup</div>
        <h1>Complete API Guide</h1>
        <p>Every AI provider explained — where to get keys, how much they cost, which is best for you</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="success-box">
    <strong>Best strategy for beginners:</strong> Start with <strong>NVIDIA Build</strong> (Gemma 4 31B — 1000 free credits!),
    <strong>OpenRouter</strong> (one key = 200+ models), or <strong>Groq</strong> (fastest free inference). All free with no credit card!
    </div>""", unsafe_allow_html=True)

    # ── FREE PROVIDERS FIRST ──
    st.markdown('<div class="section-title">Free Providers — No Credit Card Needed</div>', unsafe_allow_html=True)

    # OpenRouter
    st.markdown("""<div class="glass-card"style="background:rgba(139,92,246,0.05);border:1px solid rgba(139,92,246,0.3);border-radius:16px;padding:1.8rem;margin-bottom:1.2rem">
    <h3 style="color:#a78bfa;font-family:Syne;margin-bottom:0.8rem">OpenRouter <span style="background:rgba(16,185,129,0.15);color:#10b981;border:1px solid rgba(16,185,129,0.3);font-size:0.7rem;padding:3px 10px;border-radius:100px;font-weight:700;margin-left:10px">RECOMMENDED</span></h3>
    <p style="color:#94a3b8;margin-bottom:1rem">One API key gives you access to <strong style="color:#e2e8f0">200+ models</strong> from OpenAI, Anthropic, Google, Meta, and more. Best starting point.</p>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;margin-bottom:1rem">
        <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:1rem;border:1px solid rgba(255,255,255,0.06)">
            <div style="color:#10b981;font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em">Free Tier</div>
            <div style="color:#e2e8f0;margin-top:0.3rem">20 req/min<br>200 req/day<br>No credit card</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:1rem;border:1px solid rgba(255,255,255,0.06)">
            <div style="color:#f59e0b;font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em">Paid Tier</div>
            <div style="color:#e2e8f0;margin-top:0.3rem">Pay per token<br>Same as direct<br>No markup</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:1rem;border:1px solid rgba(255,255,255,0.06)">
            <div style="color:#a78bfa;font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em">Key Format</div>
            <div style="color:#e2e8f0;margin-top:0.3rem;font-family:monospace;font-size:0.85rem">sk-or-v1-...</div>
        </div>
    </div>
    <div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:1rem;border:1px solid rgba(255,255,255,0.05);margin-bottom:1rem">
        <div style="color:#a78bfa;font-weight:700;font-size:0.8rem;margin-bottom:0.5rem">HOW TO GET YOUR FREE KEY (2 minutes)</div>
        <div style="color:#94a3b8;font-size:0.88rem;line-height:1.8">
        1. Go to <strong style="color:#a78bfa">openrouter.ai/keys</strong><br>
        2. Click "Sign In"→ Sign up with Google (free)<br>
        3. Click "Create Key"→ give it any name<br>
        4. Copy the key (starts with <code style="background:rgba(255,255,255,0.08);padding:1px 6px;border-radius:4px">sk-or-v1-</code>)<br>
        5. Paste into this app's sidebar → done!<br>
        <br>
        <strong style="color:#e2e8f0">Tip:</strong> Use <strong>Auto Free Router</strong> as model — it never gives 404 errors!
        </div>
    </div>
    <div style="background:rgba(16,185,129,0.06);border-radius:8px;padding:0.8rem;border:1px solid rgba(16,185,129,0.2);font-size:0.82rem;color:#34d399">
    Best free models: Auto Router · Llama 3.3 70B · GPT-OSS 120B · Qwen3 Coder · NVIDIA Nemotron · Gemma 3 27B
    </div>
    </div>""", unsafe_allow_html=True)

    # Groq
    st.markdown("""<div class="glass-card"style="background:rgba(245,158,11,0.04);border:1px solid rgba(245,158,11,0.25);border-radius:16px;padding:1.8rem;margin-bottom:1.2rem">
    <h3 style="color:#fbbf24;font-family:Syne;margin-bottom:0.8rem">Groq <span style="background:rgba(16,185,129,0.15);color:#10b981;border:1px solid rgba(16,185,129,0.3);font-size:0.7rem;padding:3px 10px;border-radius:100px;font-weight:700;margin-left:10px">FASTEST FREE — 10x speed</span></h3>
    <p style="color:#94a3b8;margin-bottom:1rem">Groq runs open-source models on custom LPU chips — <strong style="color:#e2e8f0">10x faster</strong> than any other provider. Llama 3.3 70B completes in ~2 seconds vs 15+ on others.</p>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;margin-bottom:1rem">
        <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:1rem;border:1px solid rgba(255,255,255,0.06)">
            <div style="color:#10b981;font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em">Free Tier</div>
            <div style="color:#e2e8f0;margin-top:0.3rem">30 req/min<br>14,400 req/day<br>No credit card</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:1rem;border:1px solid rgba(255,255,255,0.06)">
            <div style="color:#f59e0b;font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em">Speed</div>
            <div style="color:#e2e8f0;margin-top:0.3rem">~2 sec response<br>Fastest on earth<br>LPU hardware</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:1rem;border:1px solid rgba(255,255,255,0.06)">
            <div style="color:#a78bfa;font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em">Key Format</div>
            <div style="color:#e2e8f0;margin-top:0.3rem;font-family:monospace;font-size:0.85rem">gsk_...</div>
        </div>
    </div>
    <div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:1rem;border:1px solid rgba(255,255,255,0.05)">
        <div style="color:#fbbf24;font-weight:700;font-size:0.8rem;margin-bottom:0.5rem">HOW TO GET YOUR FREE KEY</div>
        <div style="color:#94a3b8;font-size:0.88rem;line-height:1.8">
        1. Go to <strong style="color:#fbbf24">console.groq.com</strong><br>
        2. Sign up free → verify email<br>
        3. Click "API Keys"in sidebar → "Create API Key"<br>
        4. Copy key (starts with <code style="background:rgba(255,255,255,0.08);padding:1px 6px;border-radius:4px">gsk_</code>) → paste here
        </div>
    </div>
    <div style="background:rgba(245,158,11,0.06);border-radius:8px;padding:0.8rem;border:1px solid rgba(245,158,11,0.2);font-size:0.82rem;color:#fbbf24;margin-top:0.8rem">
    Best free models: Llama 3.3 70B Versatile · DeepSeek R1 Distill · Gemma2 9B · Mixtral 8x7B · Llama 3.2 Vision
    </div>
    </div>""", unsafe_allow_html=True)

    # NVIDIA Build
    st.markdown("""<div class="glass-card"style="background:rgba(118,185,0,0.04);border:1px solid rgba(118,185,0,0.3);border-radius:16px;padding:1.8rem;margin-bottom:1.2rem">
    <h3 style="color:#76b900;font-family:Syne;margin-bottom:0.8rem">NVIDIA Build <span style="background:rgba(118,185,0,0.15);color:#76b900;border:1px solid rgba(118,185,0,0.3);font-size:0.7rem;padding:3px 10px;border-radius:100px;font-weight:700;margin-left:10px">NEW — 1000 FREE CREDITS</span></h3>
    <p style="color:#94a3b8;margin-bottom:1rem">NVIDIA NIM inference — run <strong style="color:#e2e8f0">Gemma 4 31B IT</strong>, Llama 3.3 70B, and Nemotron on NVIDIA's blazing-fast GPUs. <strong style="color:#e2e8f0">1000 free API credits</strong> on signup!</p>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;margin-bottom:1rem">
        <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:1rem;border:1px solid rgba(255,255,255,0.06)">
            <div style="color:#76b900;font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em">Free Tier</div>
            <div style="color:#e2e8f0;margin-top:0.3rem">1000 free credits<br>No credit card<br>Enterprise GPUs</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:1rem;border:1px solid rgba(255,255,255,0.06)">
            <div style="color:#f59e0b;font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em">Best Model</div>
            <div style="color:#e2e8f0;margin-top:0.3rem">Gemma 4 31B IT<br>Frontier reasoning<br>Coding & agents</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:1rem;border:1px solid rgba(255,255,255,0.06)">
            <div style="color:#a78bfa;font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em">Key Format</div>
            <div style="color:#e2e8f0;margin-top:0.3rem;font-family:monospace;font-size:0.85rem">nvapi-...</div>
        </div>
    </div>
    <div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:1rem;border:1px solid rgba(255,255,255,0.05)">
        <div style="color:#76b900;font-weight:700;font-size:0.8rem;margin-bottom:0.5rem">HOW TO GET YOUR FREE KEY (2 minutes)</div>
        <div style="color:#94a3b8;font-size:0.88rem;line-height:1.8">
        1. Go to <strong style="color:#76b900">build.nvidia.com</strong><br>
        2. Click "Sign In"→ Sign up with Google or email (free)<br>
        3. Click any model (e.g. Gemma 4 31B IT) → "Get API Key"<br>
        4. Copy the key (starts with <code style="background:rgba(255,255,255,0.08);padding:1px 6px;border-radius:4px">nvapi-</code>) → paste into sidebar<br>
        5. Select <strong style="color:#e2e8f0">NVIDIA Build</strong> provider → pick Gemma 4 → go!
        </div>
    </div>
    <div style="background:rgba(118,185,0,0.06);border-radius:8px;padding:0.8rem;border:1px solid rgba(118,185,0,0.2);font-size:0.82rem;color:#76b900;margin-top:0.8rem">
    Best models: Gemma 4 31B IT · Llama 3.3 70B · Nemotron 70B · Llama 3.1 8B · Mistral 7B
    </div>
    </div>""", unsafe_allow_html=True)

    # Google Gemini
    st.markdown("""<div class="glass-card"style="background:rgba(96,165,250,0.04);border:1px solid rgba(96,165,250,0.25);border-radius:16px;padding:1.8rem;margin-bottom:1.2rem">
    <h3 style="color:#93c5fd;font-family:Syne;margin-bottom:0.8rem">Google Gemini <span style="background:rgba(16,185,129,0.15);color:#10b981;border:1px solid rgba(16,185,129,0.3);font-size:0.7rem;padding:3px 10px;border-radius:100px;font-weight:700;margin-left:10px">FREE — 1M tokens/day</span></h3>
    <p style="color:#94a3b8;margin-bottom:1rem">Official Google API — Gemini 2.0 Flash is free and extremely capable. <strong style="color:#e2e8f0">1 million tokens/day free</strong> — that's 1000+ resume analyses!</p>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;margin-bottom:1rem">
        <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:1rem;border:1px solid rgba(255,255,255,0.06)">
            <div style="color:#10b981;font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em">Free Tier</div>
            <div style="color:#e2e8f0;margin-top:0.3rem">15 req/min<br>1M tokens/day<br>No credit card</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:1rem;border:1px solid rgba(255,255,255,0.06)">
            <div style="color:#f59e0b;font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em">Paid Models</div>
            <div style="color:#e2e8f0;margin-top:0.3rem">Gemini 1.5 Pro<br>$1.25/$5 per M<br>2M ctx window</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:1rem;border:1px solid rgba(255,255,255,0.06)">
            <div style="color:#a78bfa;font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em">Key Format</div>
            <div style="color:#e2e8f0;margin-top:0.3rem;font-family:monospace;font-size:0.85rem">AIza...</div>
        </div>
    </div>
    <div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:1rem;border:1px solid rgba(255,255,255,0.05)">
        <div style="color:#93c5fd;font-weight:700;font-size:0.8rem;margin-bottom:0.5rem">HOW TO GET YOUR FREE KEY</div>
        <div style="color:#94a3b8;font-size:0.88rem;line-height:1.8">
        1. Go to <strong style="color:#93c5fd">aistudio.google.com/app/apikey</strong><br>
        2. Sign in with Google account (free)<br>
        3. Click "Create API Key"→ copy it (starts with <code style="background:rgba(255,255,255,0.08);padding:1px 6px;border-radius:4px">AIza</code>)<br>
        4. Paste into this app → select Google Gemini provider
        </div>
    </div>
    </div>""", unsafe_allow_html=True)

    # Hugging Face
    st.markdown("""<div class="glass-card"style="background:rgba(251,191,36,0.04);border:1px solid rgba(251,191,36,0.2);border-radius:16px;padding:1.8rem;margin-bottom:1.2rem">
    <h3 style="color:#fde68a;font-family:Syne;margin-bottom:0.8rem">Hugging Face <span style="background:rgba(16,185,129,0.15);color:#10b981;border:1px solid rgba(16,185,129,0.3);font-size:0.7rem;padding:3px 10px;border-radius:100px;font-weight:700;margin-left:10px">FREE Serverless API</span></h3>
    <p style="color:#94a3b8;margin-bottom:1rem">World's largest open-source AI hub. Free Serverless Inference API for popular models — no setup needed.</p>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;margin-bottom:1rem">
        <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:1rem;border:1px solid rgba(255,255,255,0.06)">
            <div style="color:#10b981;font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em">Free Tier</div>
            <div style="color:#e2e8f0;margin-top:0.3rem">Free inference<br>Rate limited<br>No credit card</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:1rem;border:1px solid rgba(255,255,255,0.06)">
            <div style="color:#f59e0b;font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em">Models</div>
            <div style="color:#e2e8f0;margin-top:0.3rem">Llama 3.1 8B<br>Gemma 2 9B<br>Qwen 2.5 7B</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:1rem;border:1px solid rgba(255,255,255,0.06)">
            <div style="color:#a78bfa;font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em">Key Format</div>
            <div style="color:#e2e8f0;margin-top:0.3rem;font-family:monospace;font-size:0.85rem">hf_...</div>
        </div>
    </div>
    <div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:1rem;border:1px solid rgba(255,255,255,0.05)">
        <div style="color:#fde68a;font-weight:700;font-size:0.8rem;margin-bottom:0.5rem">HOW TO GET YOUR FREE KEY</div>
        <div style="color:#94a3b8;font-size:0.88rem;line-height:1.8">
        1. Go to <strong style="color:#fde68a">huggingface.co/settings/tokens</strong><br>
        2. Create free account → Settings → Access Tokens<br>
        3. Create new token (type: "Read") → copy key (starts with <code style="background:rgba(255,255,255,0.08);padding:1px 6px;border-radius:4px">hf_</code>)<br>
        4. Note: Some models may take 30s to load ("cold start")
        </div>
    </div>
    </div>""", unsafe_allow_html=True)

    # Cohere
    st.markdown("""<div class="glass-card"style="background:rgba(52,211,153,0.04);border:1px solid rgba(52,211,153,0.2);border-radius:16px;padding:1.8rem;margin-bottom:1.2rem">
    <h3 style="color:#6ee7b7;font-family:Syne;margin-bottom:0.8rem">Cohere <span style="background:rgba(16,185,129,0.15);color:#10b981;border:1px solid rgba(16,185,129,0.3);font-size:0.7rem;padding:3px 10px;border-radius:100px;font-weight:700;margin-left:10px">FREE 1000 req/month</span></h3>
    <p style="color:#94a3b8;margin-bottom:1rem">Excellent for document analysis and RAG. Command R is their free flagship — great for resume analysis.</p>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;margin-bottom:1rem">
        <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:1rem;border:1px solid rgba(255,255,255,0.06)">
            <div style="color:#10b981;font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em">Free Tier</div>
            <div style="color:#e2e8f0;margin-top:0.3rem">20 req/min<br>1000 req/month<br>No credit card</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:1rem;border:1px solid rgba(255,255,255,0.06)">
            <div style="color:#f59e0b;font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em">Paid</div>
            <div style="color:#e2e8f0;margin-top:0.3rem">Command R+<br>$2.5/$10 per M<br>Enterprise ready</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:1rem;border:1px solid rgba(255,255,255,0.06)">
            <div style="color:#a78bfa;font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em">Key Format</div>
            <div style="color:#e2e8f0;margin-top:0.3rem;font-family:monospace;font-size:0.85rem">random string</div>
        </div>
    </div>
    <div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:1rem;border:1px solid rgba(255,255,255,0.05)">
        <div style="color:#6ee7b7;font-weight:700;font-size:0.8rem;margin-bottom:0.5rem">HOW TO GET YOUR FREE KEY</div>
        <div style="color:#94a3b8;font-size:0.88rem;line-height:1.8">
        1. Go to <strong style="color:#6ee7b7">dashboard.cohere.com</strong><br>
        2. Sign up free → API Keys section<br>
        3. Copy your Trial API key<br>
        4. Select Cohere provider in sidebar
        </div>
    </div>
    </div>""", unsafe_allow_html=True)

    # ── PAID / CREDITS PROVIDERS ──
    st.markdown('<div class="section-title">Paid Providers — Best Quality (some have free credits on signup)</div>', unsafe_allow_html=True)

    # Pricing table
    st.markdown("""<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:1.5rem;margin-bottom:1.2rem;overflow-x:auto">
    <table style="width:100%;border-collapse:collapse;font-size:0.85rem">
        <thead>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.1)">
                <th style="text-align:left;padding:10px;color:#a78bfa;font-family:Syne;letter-spacing:0.05em">Provider</th>
                <th style="text-align:left;padding:10px;color:#a78bfa;font-family:Syne;letter-spacing:0.05em">Free Credits</th>
                <th style="text-align:left;padding:10px;color:#a78bfa;font-family:Syne;letter-spacing:0.05em">Best Model</th>
                <th style="text-align:left;padding:10px;color:#a78bfa;font-family:Syne;letter-spacing:0.05em">Cost/Resume*</th>
                <th style="text-align:left;padding:10px;color:#a78bfa;font-family:Syne;letter-spacing:0.05em">Get Key</th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.05)">
                <td style="padding:10px;color:#e2e8f0">Anthropic</td>
                <td style="padding:10px;color:#ef4444">None</td>
                <td style="padding:10px;color:#e2e8f0">Claude 3.5 Sonnet</td>
                <td style="padding:10px;color:#f59e0b">~$0.005</td>
                <td style="padding:10px"><a href="https://console.anthropic.com"target="_blank"style="color:#a78bfa;text-decoration:none">console.anthropic.com</a></td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.05)">
                <td style="padding:10px;color:#e2e8f0">OpenAI</td>
                <td style="padding:10px;color:#f59e0b">~$5 new accounts</td>
                <td style="padding:10px;color:#e2e8f0">GPT-4o Mini</td>
                <td style="padding:10px;color:#10b981">~$0.0003</td>
                <td style="padding:10px"><a href="https://platform.openai.com/api-keys"target="_blank"style="color:#a78bfa;text-decoration:none">platform.openai.com</a></td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.05)">
                <td style="padding:10px;color:#e2e8f0">DeepSeek</td>
                <td style="padding:10px;color:#f59e0b">~$5 new accounts</td>
                <td style="padding:10px;color:#e2e8f0">DeepSeek R1</td>
                <td style="padding:10px;color:#10b981">~$0.001</td>
                <td style="padding:10px"><a href="https://platform.deepseek.com"target="_blank"style="color:#a78bfa;text-decoration:none">platform.deepseek.com</a></td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.05)">
                <td style="padding:10px;color:#e2e8f0">Together AI</td>
                <td style="padding:10px;color:#10b981">$25 free!</td>
                <td style="padding:10px;color:#e2e8f0">Llama 3.3 70B Turbo</td>
                <td style="padding:10px;color:#10b981">~$0.002</td>
                <td style="padding:10px"><a href="https://api.together.xyz"target="_blank"style="color:#a78bfa;text-decoration:none">api.together.xyz</a></td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.05)">
                <td style="padding:10px;color:#e2e8f0">xAI Grok</td>
                <td style="padding:10px;color:#10b981">$25 free!</td>
                <td style="padding:10px;color:#e2e8f0">Grok 3 Mini</td>
                <td style="padding:10px;color:#10b981">~$0.001</td>
                <td style="padding:10px"><a href="https://console.x.ai"target="_blank"style="color:#a78bfa;text-decoration:none">console.x.ai</a></td>
            </tr>
            <tr style="border-bottom:1px solid rgba(255,255,255,0.05)">
                <td style="padding:10px;color:#e2e8f0">Mistral AI</td>
                <td style="padding:10px;color:#f59e0b">Free trial credits</td>
                <td style="padding:10px;color:#e2e8f0">Mistral Small</td>
                <td style="padding:10px;color:#10b981">~$0.0002</td>
                <td style="padding:10px"><a href="https://console.mistral.ai"target="_blank"style="color:#a78bfa;text-decoration:none">console.mistral.ai</a></td>
            </tr>
            <tr>
                <td style="padding:10px;color:#e2e8f0">Perplexity</td>
                <td style="padding:10px;color:#ef4444">None</td>
                <td style="padding:10px;color:#e2e8f0">Sonar (web search!)</td>
                <td style="padding:10px;color:#f59e0b">~$0.005</td>
                <td style="padding:10px"><a href="https://www.perplexity.ai/settings/api"target="_blank"style="color:#a78bfa;text-decoration:none">perplexity.ai/api</a></td>
            </tr>
        </tbody>
    </table>
    <p style="color:#475569;font-size:0.75rem;margin-top:0.8rem">* Estimated cost per resume analysis (~2000 tokens input + 500 output)</p>
    </div>""", unsafe_allow_html=True)

    # ── MODEL COMPARISON ──
    st.markdown('<div class="section-title">Which Model Should You Use?</div>', unsafe_allow_html=True)
    st.markdown("""<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem">
        <div class="info-box">
        <strong>Best Free Setup (Zero Cost):</strong><br><br>
        1st choice: <strong>NVIDIA Build</strong> → Gemma 4 31B IT (best quality)<br>
        2nd choice: <strong>OpenRouter</strong> → Auto Free Router<br>
        3rd choice: <strong>Groq</strong> → Llama 3.3 70B (fastest)<br>
        4th choice: <strong>Google Gemini</strong> → Gemini 2.0 Flash<br><br>
        All four give excellent results — completely free!
        </div>
        <div class="info-box">
        <strong>Best Paid Setup (Best Results):</strong><br><br>
        Best quality: <strong>Claude 3.5 Sonnet</strong> via Anthropic or OpenRouter<br>
        Best value: <strong>DeepSeek R1</strong> (~$0.001 per analysis!)<br>
        Most features: <strong>Perplexity Sonar</strong> (has web search)<br><br>
        Start with free, upgrade when you want even better analysis!
        </div>
    </div>""", unsafe_allow_html=True)

    # ── TROUBLESHOOTING ──
    st.markdown('<div class="section-title">Common Errors & Fixes</div>', unsafe_allow_html=True)
    st.markdown("""
| Error | Cause | Fix |
|-------|-------|-----|
| `401 Unauthorized` | Wrong API key | Double-check key, no extra spaces |
| `404 Not Found` | Model removed/renamed | Switch to Auto Free Router |
| `429 Rate Limit` | Too many requests | Wait 1 min or switch model |
| `402 Payment Required` | No credits | Add credits or use free model |
| `503 Service Unavailable` | Model loading | Wait 30 sec (HuggingFace cold start) |
| `timeout` | Slow model | Switch to Groq for fastest responses |
    """)

    # ── CHEAPEST WAY ──
    st.markdown("""<div class="win-box">
    <strong>Absolute cheapest paid option:</strong> DeepSeek V3 via DeepSeek API costs ~$0.00027 per 1000 tokens.
    A full resume analysis costs less than <strong>$0.001</strong> — literally 1000 analyses for $1.
    Get $5 free credits at platform.deepseek.com = <strong>5000 free analyses!</strong>
    </div>""", unsafe_allow_html=True)

    # ── LOCAL LLM SECTION ──
    st.markdown('<div class="section-title">Local LLM — Run AI on Your Own Machine (100% Free + Private)</div>', unsafe_allow_html=True)

    st.markdown("""<div style="background:rgba(16,185,129,0.05);border:1px solid rgba(16,185,129,0.25);border-radius:16px;padding:1.8rem;margin-bottom:1.2rem">
    <h3 style="font-family:Syne,sans-serif;color:#34d399;margin-bottom:0.5rem">Ollama <span style="background:rgba(16,185,129,0.15);color:#10b981;border:1px solid rgba(16,185,129,0.3);font-size:0.7rem;padding:3px 10px;border-radius:100px;font-weight:700;margin-left:10px">EASIEST LOCAL OPTION</span></h3>
    <p style="color:#94a3b8;margin-bottom:1rem">Ollama runs open-source models (Llama, DeepSeek, Gemma, Mistral, Phi) directly on your CPU or GPU. Zero cost forever. Zero privacy risk — nothing leaves your machine.</p>

    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.8rem;margin-bottom:1.2rem">
        <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:0.9rem;border:1px solid rgba(255,255,255,0.06)">
            <div style="color:#10b981;font-weight:700;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.08em">Cost</div>
            <div style="color:#e2e8f0;margin-top:0.3rem;font-size:0.88rem">$0 forever<br>No API key<br>No internet</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:0.9rem;border:1px solid rgba(255,255,255,0.06)">
            <div style="color:#f59e0b;font-weight:700;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.08em">Requirements</div>
            <div style="color:#e2e8f0;margin-top:0.3rem;font-size:0.88rem">8GB RAM min<br>16GB for 7B<br>32GB+ for 14B+</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:0.9rem;border:1px solid rgba(255,255,255,0.06)">
            <div style="color:#a78bfa;font-weight:700;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.08em">Where it works</div>
            <div style="color:#e2e8f0;margin-top:0.3rem;font-size:0.88rem">Run app locally<br>Streamlit Cloud<br>Your laptop/PC</div>
        </div>
    </div>

    <div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:1.2rem;border:1px solid rgba(255,255,255,0.06);margin-bottom:1rem">
        <div style="color:#34d399;font-weight:700;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.8rem">SETUP IN 5 STEPS (~5 minutes)</div>

        <div style="font-size:0.86rem;color:#94a3b8;line-height:2.1">
        <span style="color:#34d399;font-weight:700">Step 1</span> — Download Ollama:
        <code style="background:rgba(255,255,255,0.08);padding:2px 8px;border-radius:5px;color:#a78bfa">ollama.com/download</code> (Mac / Windows / Linux)<br>

        <span style="color:#34d399;font-weight:700">Step 2</span> — Install it (just double-click the installer)<br>

        <span style="color:#34d399;font-weight:700">Step 3</span> — Open Terminal / Command Prompt and pull a model:<br>
        &nbsp;&nbsp;&nbsp;&nbsp;<code style="background:rgba(255,255,255,0.08);padding:2px 8px;border-radius:5px;color:#a78bfa">ollama pull llama3.2</code> &nbsp; ← 2GB, good for most computers<br>
        &nbsp;&nbsp;&nbsp;&nbsp;<code style="background:rgba(255,255,255,0.08);padding:2px 8px;border-radius:5px;color:#a78bfa">ollama pull deepseek-r1:7b</code> &nbsp; ← 4GB, best reasoning<br>
        &nbsp;&nbsp;&nbsp;&nbsp;<code style="background:rgba(255,255,255,0.08);padding:2px 8px;border-radius:5px;color:#a78bfa">ollama pull phi3.5</code> &nbsp; ← 2GB, fastest on low RAM<br>

        <span style="color:#34d399;font-weight:700">Step 4</span> — Start Ollama server:
        <code style="background:rgba(255,255,255,0.08);padding:2px 8px;border-radius:5px;color:#a78bfa">ollama serve</code><br>

        <span style="color:#34d399;font-weight:700">Step 5</span> — Run this app locally:
        <code style="background:rgba(255,255,255,0.08);padding:2px 8px;border-radius:5px;color:#a78bfa">streamlit run app.py</code>
        → Select <strong style="color:#e2e8f0">Ollama (Local)</strong> in sidebar → pick your model → done!
        </div>
    </div>

    <div style="background:rgba(139,92,246,0.06);border-radius:10px;padding:1rem;border:1px solid rgba(139,92,246,0.2);margin-bottom:0.8rem">
        <div style="color:#a78bfa;font-weight:700;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.6rem">WHICH MODEL TO USE?</div>
        <div style="font-size:0.84rem;color:#94a3b8;line-height:1.9">
        <strong style="color:#e2e8f0">8GB RAM laptop:</strong> <code style="background:rgba(255,255,255,0.07);padding:1px 6px;border-radius:4px;color:#a78bfa">ollama pull phi3.5</code> or <code style="background:rgba(255,255,255,0.07);padding:1px 6px;border-radius:4px;color:#a78bfa">llama3.2</code> (2-3GB)<br>
        <strong style="color:#e2e8f0">16GB RAM:</strong> <code style="background:rgba(255,255,255,0.07);padding:1px 6px;border-radius:4px;color:#a78bfa">ollama pull llama3.1</code> or <code style="background:rgba(255,255,255,0.07);padding:1px 6px;border-radius:4px;color:#a78bfa">deepseek-r1:7b</code> (4-5GB) ← best quality/speed<br>
        <strong style="color:#e2e8f0">32GB RAM or GPU:</strong> <code style="background:rgba(255,255,255,0.07);padding:1px 6px;border-radius:4px;color:#a78bfa">ollama pull qwen2.5:14b</code> or <code style="background:rgba(255,255,255,0.07);padding:1px 6px;border-radius:4px;color:#a78bfa">deepseek-r1:14b</code> (8-9GB)<br>
        <strong style="color:#e2e8f0">NVIDIA GPU (8GB+ VRAM):</strong> Ollama auto-detects GPU — blazing fast!
        </div>
    </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div style="background:rgba(245,158,11,0.04);border:1px solid rgba(245,158,11,0.2);border-radius:16px;padding:1.8rem;margin-bottom:1.2rem">
    <h3 style="font-family:Syne,sans-serif;color:#fbbf24;margin-bottom:0.5rem">LM Studio <span style="background:rgba(245,158,11,0.12);color:#f59e0b;border:1px solid rgba(245,158,11,0.25);font-size:0.7rem;padding:3px 10px;border-radius:100px;font-weight:700;margin-left:10px">Drag & Drop ANY GGUF File</span></h3>
    <p style="color:#94a3b8;margin-bottom:1rem">LM Studio has a beautiful GUI — browse HuggingFace, download any GGUF model, and load it with one click. Exposes an OpenAI-compatible local server.</p>

    <div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:1.2rem;border:1px solid rgba(255,255,255,0.06)">
        <div style="color:#fbbf24;font-weight:700;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.8rem">SETUP IN 4 STEPS</div>
        <div style="font-size:0.86rem;color:#94a3b8;line-height:2.1">
        <span style="color:#fbbf24;font-weight:700">Step 1</span> — Download LM Studio from <code style="background:rgba(255,255,255,0.08);padding:2px 8px;border-radius:5px;color:#a78bfa">lmstudio.ai</code><br>
        <span style="color:#fbbf24;font-weight:700">Step 2</span> — Inside LM Studio: search for any model (e.g. "Llama"or "Mistral") → Download<br>
        &nbsp;&nbsp;&nbsp;&nbsp;Or drag & drop your own .gguf file into the app window<br>
        <span style="color:#fbbf24;font-weight:700">Step 3</span> — Click <strong style="color:#e2e8f0">"Local Server"</strong> tab → click <strong style="color:#e2e8f0">Start Server</strong><br>
        <span style="color:#fbbf24;font-weight:700">Step 4</span> — In this app: select <strong style="color:#e2e8f0">LM Studio (Local)</strong> → no key needed → use!
        </div>
    </div>

    <div style="background:rgba(16,185,129,0.06);border-radius:8px;padding:0.8rem;font-size:0.82rem;color:#34d399;margin-top:0.8rem">
    <strong>Best for:</strong> Trying many different GGUF models from HuggingFace without using terminal commands
    </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div style="background:rgba(139,92,246,0.06);border:1px solid rgba(139,92,246,0.2);border-radius:14px;padding:1.2rem;margin-bottom:1rem">
    <div style="font-family:Syne,sans-serif;font-weight:700;color:#a78bfa;margin-bottom:0.8rem">Local vs Cloud — When to Use What?</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;font-size:0.84rem">
        <div>
        <div style="color:#10b981;font-weight:600;margin-bottom:0.4rem">Use Local (Ollama/LM Studio) when:</div>
        <div style="color:#94a3b8;line-height:1.8">• Your resume has sensitive personal info<br>• You want zero API cost forever<br>• You have 8GB+ RAM on your machine<br>• You want to run offline (no internet)<br>• You want to try cutting-edge new models</div>
        </div>
        <div>
        <div style="color:#a78bfa;font-weight:600;margin-bottom:0.4rem">Use Cloud APIs (OpenRouter/Groq) when:</div>
        <div style="color:#94a3b8;line-height:1.8">• You're using Streamlit Cloud (deployed)<br>• You want the fastest response time<br>• You have a low-spec laptop (&lt;8GB RAM)<br>• You want the absolute best quality (Claude)<br>• You're sharing the app with others</div>
        </div>
    </div>
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
# HOW TO USE
# ════════════════════════════════════════════════════════
elif page == "How to Use":
    st.markdown("""<div class="hero">
        <div class="hero-badge">Step-by-Step · Beginner Friendly · 5 Tools</div>
        <h1>How to Use This App</h1>
        <p>New here? This page walks you through everything — from getting your free API key to landing more interviews</p>
    </div>""", unsafe_allow_html=True)

    # ── STEP 0: GET STARTED ──
    st.markdown('<div class="section-title">Before You Start — Get Your Free API Key (2 minutes)</div>', unsafe_allow_html=True)
    st.markdown("""
<div style="background:linear-gradient(135deg,rgba(139,92,246,0.08),rgba(16,185,129,0.05));border:1px solid rgba(139,92,246,0.3);border-radius:16px;padding:1.8rem;margin-bottom:1.5rem">
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;margin-bottom:1.2rem">

<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(139,92,246,0.2);border-radius:12px;padding:1.2rem;text-align:center">
  <div style="font-size:2rem;margin-bottom:0.5rem"></div>
  <div style="font-family:Syne,sans-serif;font-weight:700;color:#a78bfa;margin-bottom:0.4rem">Go to OpenRouter</div>
  <div style="font-size:0.82rem;color:#94a3b8;line-height:1.6">Visit<br><strong style="color:#e2e8f0">openrouter.ai/keys</strong><br>in your browser</div>
</div>

<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(139,92,246,0.2);border-radius:12px;padding:1.2rem;text-align:center">
  <div style="font-size:2rem;margin-bottom:0.5rem"></div>
  <div style="font-family:Syne,sans-serif;font-weight:700;color:#a78bfa;margin-bottom:0.4rem">Sign Up Free</div>
  <div style="font-size:0.82rem;color:#94a3b8;line-height:1.6">Click Sign In<br>Sign up with Google<br><strong style="color:#10b981">No credit card needed</strong></div>
</div>

<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(139,92,246,0.2);border-radius:12px;padding:1.2rem;text-align:center">
  <div style="font-size:2rem;margin-bottom:0.5rem"></div>
  <div style="font-family:Syne,sans-serif;font-weight:700;color:#a78bfa;margin-bottom:0.4rem">Create & Paste Key</div>
  <div style="font-size:0.82rem;color:#94a3b8;line-height:1.6">Click "Create Key"<br>Copy it (starts <code style="background:rgba(255,255,255,0.1);padding:1px 5px;border-radius:3px;font-size:0.75rem">sk-or-v1-</code>)<br>Paste in the sidebar ←</div>
</div>

</div>
<div style="background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.25);border-radius:10px;padding:1rem;font-size:0.88rem;color:#e2e8f0">
<strong>That's it!</strong> You're now ready to use all 5 tools completely free.
In the sidebar: select <strong>OpenRouter</strong> → keep model as <strong>Auto Free Router</strong> → you're set!
</div>
</div>
""", unsafe_allow_html=True)

    # ── TOOL 1: ANALYZER ──
    st.markdown('<div class="section-title">Tool 1 — Resume Analyzer</div>', unsafe_allow_html=True)
    st.markdown("""
<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:1.8rem;margin-bottom:1.2rem">

<div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.2rem;flex-wrap:wrap">
  <div style="font-size:2.5rem"></div>
  <div>
    <div style="font-family:Syne,sans-serif;font-size:1.2rem;font-weight:700;color:#e2e8f0">Resume Analyzer</div>
    <div style="color:#94a3b8;font-size:0.88rem">Get your ATS score, job match %, interview probability, red flags & salary insight</div>
  </div>
  <div style="margin-left:auto">
    <span style="background:rgba(16,185,129,0.12);color:#10b981;border:1px solid rgba(16,185,129,0.3);padding:4px 12px;border-radius:100px;font-size:0.75rem;font-weight:700">~15 seconds</span>
  </div>
</div>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1.2rem">
<div>
<div style="color:#a78bfa;font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.6rem">HOW TO USE</div>
<div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:1rem;font-size:0.86rem;color:#94a3b8;line-height:2">
<span style="color:#a78bfa;font-weight:700">Step 1</span> — Upload your resume PDF <em>or</em> paste resume text<br>
<span style="color:#a78bfa;font-weight:700">Step 2</span> — Type the job title (e.g. "Data Engineer")<br>
<span style="color:#a78bfa;font-weight:700">Step 3</span> — Paste the full job description from LinkedIn/Indeed<br>
<span style="color:#a78bfa;font-weight:700">Step 4</span> — Click <strong style="color:#e2e8f0">Analyze My Resume</strong><br>
<span style="color:#a78bfa;font-weight:700">Step 5</span> — Download the full report as .txt
</div>
</div>
<div>
<div style="color:#10b981;font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.6rem">WHAT YOU GET</div>
<div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:1rem;font-size:0.86rem;color:#94a3b8;line-height:2">
<strong style="color:#e2e8f0">ATS Score</strong> — how ATS robots rate your resume<br>
<strong style="color:#e2e8f0">Job Match %</strong> — how well you fit the role<br>
<strong style="color:#e2e8f0">Interview Probability</strong> — realistic callback chance<br>
<strong style="color:#e2e8f0">Matched & Missing Skills</strong> — keyword gaps<br>
<strong style="color:#e2e8f0">Quick Wins</strong> — fix these TODAY for more callbacks<br>
<strong style="color:#e2e8f0">Red Flags</strong> — what recruiters notice negatively<br>
<strong style="color:#e2e8f0">Salary Insight</strong> — your estimated market value<br>
<strong style="color:#e2e8f0">Deep Analysis</strong> — competitive positioning, section grades, AI rewrites
</div>
</div>
</div>

<div style="background:rgba(245,158,11,0.07);border:1px solid rgba(245,158,11,0.2);border-radius:10px;padding:0.9rem;font-size:0.85rem;color:#fbbf24">
<strong>Pro Tip:</strong> Paste the COMPLETE job description — not just the title. The more text you give, the more accurate the keyword matching. Aim for <strong>ATS score 80+</strong> before applying!
</div>
</div>
""", unsafe_allow_html=True)

    # ── TOOL 2: COVER LETTER ──
    st.markdown('<div class="section-title">Tool 2 — Smart Letter Generator</div>', unsafe_allow_html=True)
    st.markdown("""
<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:1.8rem;margin-bottom:1.2rem">

<div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.2rem;flex-wrap:wrap">
  <div style="font-size:2.5rem"></div>
  <div>
    <div style="font-family:Syne,sans-serif;font-size:1.2rem;font-weight:700;color:#e2e8f0">Smart Letter Generator</div>
    <div style="color:#94a3b8;font-size:0.88rem">Cover letters, follow-up emails, thank-you notes, LinkedIn messages, and cold outreach — all AI-powered</div>
  </div>
  <div style="margin-left:auto">
    <span style="background:rgba(16,185,129,0.12);color:#10b981;border:1px solid rgba(16,185,129,0.3);padding:4px 12px;border-radius:100px;font-size:0.75rem;font-weight:700">~20 seconds</span>
  </div>
</div>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1.2rem">
<div>
<div style="color:#a78bfa;font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.6rem">HOW TO USE</div>
<div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:1rem;font-size:0.86rem;color:#94a3b8;line-height:2">
<span style="color:#a78bfa;font-weight:700">Step 1</span> — Upload/paste your resume<br>
<span style="color:#a78bfa;font-weight:700">Step 2</span> — Enter Job Title & Company name<br>
<span style="color:#a78bfa;font-weight:700">Step 3</span> — Add hiring manager name (optional but helps!)<br>
<span style="color:#a78bfa;font-weight:700">Step 4</span> — Paste the job description<br>
<span style="color:#a78bfa;font-weight:700">Step 5</span> — Choose your tone (Formal / Professional / Friendly)<br>
<span style="color:#a78bfa;font-weight:700">Step 6</span> — Click Generate → Download .txt
</div>
</div>
<div>
<div style="color:#10b981;font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.6rem">WHAT MAKES IT SPECIAL</div>
<div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:1rem;font-size:0.86rem;color:#94a3b8;line-height:2">
Starts with a strong hook (not "I am writing to apply")<br>
Uses YOUR actual achievements from resume<br>
Injects 5 ATS keywords from the job description<br>
Personalized to the specific company<br>
Right length — 3-4 paragraphs, ~380 words<br>
Sounds human, not generic AI
</div>
</div>
</div>

<div style="background:rgba(96,165,250,0.07);border:1px solid rgba(96,165,250,0.2);border-radius:10px;padding:0.9rem;font-size:0.85rem;color:#93c5fd">
<strong>After downloading:</strong> Copy into Google Docs → add your name/address header at top → save as PDF → ready to send! Don't forget to personalize 1-2 lines with something specific about the company.
</div>
</div>
""", unsafe_allow_html=True)

    # ── TOOL 3: INTERVIEW PREP ──
    st.markdown('<div class="section-title">Tool 3 — Interview Prep Guide</div>', unsafe_allow_html=True)
    st.markdown("""
<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:1.8rem;margin-bottom:1.2rem">

<div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.2rem;flex-wrap:wrap">
  <div style="font-size:2.5rem"></div>
  <div>
    <div style="font-family:Syne,sans-serif;font-size:1.2rem;font-weight:700;color:#e2e8f0">Interview Prep Guide</div>
    <div style="color:#94a3b8;font-size:0.88rem">Questions and ideal answers based on YOUR resume — not generic ones from Google</div>
  </div>
  <div style="margin-left:auto">
    <span style="background:rgba(16,185,129,0.12);color:#10b981;border:1px solid rgba(16,185,129,0.3);padding:4px 12px;border-radius:100px;font-size:0.75rem;font-weight:700">~25 seconds</span>
  </div>
</div>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1.2rem">
<div>
<div style="color:#a78bfa;font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.6rem">HOW TO USE</div>
<div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:1rem;font-size:0.86rem;color:#94a3b8;line-height:2">
<span style="color:#a78bfa;font-weight:700">Step 1</span> — Upload/paste your resume<br>
<span style="color:#a78bfa;font-weight:700">Step 2</span> — Enter Job Title & Company<br>
<span style="color:#a78bfa;font-weight:700">Step 3</span> — Paste the job description<br>
<span style="color:#a78bfa;font-weight:700">Step 4</span> — Check which question types you want:<br>
&nbsp;&nbsp;&nbsp;&nbsp;Technical · Behavioral · Situational · Company Fit<br>
<span style="color:#a78bfa;font-weight:700">Step 5</span> — Choose 2–5 questions per category<br>
<span style="color:#a78bfa;font-weight:700">Step 6</span> — Generate → Download → Practice!
</div>
</div>
<div>
<div style="color:#10b981;font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.6rem">EACH QUESTION INCLUDES</div>
<div style="background:rgba(255,255,255,0.02);border-radius:10px;padding:1rem;font-size:0.86rem;color:#94a3b8;line-height:2">
The actual question (specific to YOUR experience)<br>
Why interviewers ask this (so you understand intent)<br>
Ideal answer framework (3-4 bullets using your resume)<br>
Common mistake to avoid (so you don't fail)<br>
<br>
<em style="color:#64748b">Questions reference your actual projects, companies, and skills — not generic ones!</em>
</div>
</div>
</div>

<div style="background:rgba(16,185,129,0.07);border:1px solid rgba(16,185,129,0.2);border-radius:10px;padding:0.9rem;font-size:0.85rem;color:#34d399">
<strong>Best practice:</strong> Download the guide → Print it → Practice each answer OUT LOUD 3 times → Record yourself on your phone → Watch it back. This alone increases interview success by 40%!
</div>
</div>
""", unsafe_allow_html=True)

    # ── TOOL 4: RESUME BUILDER ──
    st.markdown('<div class="section-title">Tool 4 — AI Resume Builder</div>', unsafe_allow_html=True)
    st.markdown("""
<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:1.8rem;margin-bottom:1.2rem">

<div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.2rem;flex-wrap:wrap">
  <div style="font-size:2.5rem"></div>
  <div>
    <div style="font-family:Syne,sans-serif;font-size:1.2rem;font-weight:700;color:#e2e8f0">AI Resume Builder</div>
    <div style="color:#94a3b8;font-size:0.88rem">Two powerful modes: Build from scratch OR rewrite your existing resume for any new job</div>
  </div>
  <div style="margin-left:auto">
    <span style="background:rgba(16,185,129,0.12);color:#10b981;border:1px solid rgba(16,185,129,0.3);padding:4px 12px;border-radius:100px;font-size:0.75rem;font-weight:700">~25 seconds</span>
  </div>
</div>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1.2rem">

<div style="background:rgba(139,92,246,0.05);border:1px solid rgba(139,92,246,0.2);border-radius:12px;padding:1.2rem">
<div style="color:#a78bfa;font-size:0.8rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.8rem">MODE 1: Build Fresh Resume</div>
<div style="font-size:0.86rem;color:#94a3b8;line-height:1.9">
<span style="color:#a78bfa">→</span> Fill in your info (name, email, edu, experience, skills)<br>
<span style="color:#a78bfa">→</span> Optionally paste a target job description<br>
<span style="color:#a78bfa">→</span> AI builds a complete ATS-optimized resume<br>
<span style="color:#a78bfa">→</span> Download as .txt → copy into Google Docs<br>
<span style="color:#a78bfa">→</span> Go to Analyzer → check your ATS score!<br>
<br>
<em style="color:#64748b">Best for: students, career changers, first resume</em>
</div>
</div>

<div style="background:rgba(16,185,129,0.05);border:1px solid rgba(16,185,129,0.2);border-radius:12px;padding:1.2rem">
<div style="color:#10b981;font-size:0.8rem;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.8rem">MODE 2: Rewrite for New Job</div>
<div style="font-size:0.86rem;color:#94a3b8;line-height:1.9">
<span style="color:#10b981">→</span> Upload/paste your CURRENT resume<br>
<span style="color:#10b981">→</span> Paste the target job description<br>
<span style="color:#10b981">→</span> Choose rewrite options (ATS keywords / metrics / language)<br>
<span style="color:#10b981">→</span> AI rewrites your ENTIRE resume for that job<br>
<span style="color:#10b981">→</span> Download both versions to compare<br>
<br>
<em style="color:#64748b">Best for: applying to multiple different roles</em>
</div>
</div>
</div>

<div style="background:rgba(245,158,11,0.07);border:1px solid rgba(245,158,11,0.2);border-radius:10px;padding:0.9rem;font-size:0.85rem;color:#fbbf24;margin-bottom:0.8rem">
<strong>Power workflow:</strong> Use Rewrite mode → download → paste back into Analyzer → check ATS score → if under 80%, rewrite again with more aggressive options. Repeat until 80+!
</div>

<div style="background:rgba(239,68,68,0.06);border:1px solid rgba(239,68,68,0.15);border-radius:10px;padding:0.9rem;font-size:0.85rem;color:#f87171">
<strong>Important:</strong> AI keeps your facts 100% accurate but optimizes language. Never let AI invent jobs, degrees, or certifications that don't exist — this is resume fraud!
</div>
</div>
""", unsafe_allow_html=True)

    # ── TOOL 5: DASHBOARD ──
    st.markdown('<div class="section-title">Tool 5 — Progress Dashboard</div>', unsafe_allow_html=True)
    st.markdown("""
<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:1.8rem;margin-bottom:1.2rem">

<div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.2rem;flex-wrap:wrap">
  <div style="font-size:2.5rem"></div>
  <div>
    <div style="font-family:Syne,sans-serif;font-size:1.2rem;font-weight:700;color:#e2e8f0">Progress Dashboard</div>
    <div style="color:#94a3b8;font-size:0.88rem">Track all your analyses, see score trends, and discover which skills you keep missing</div>
  </div>
</div>

<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.8rem;margin-bottom:1.2rem">

<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:1rem;text-align:center">
  <div style="font-size:1.5rem;margin-bottom:0.4rem"></div>
  <div style="color:#e2e8f0;font-size:0.82rem;font-weight:600">Score Trends</div>
  <div style="color:#64748b;font-size:0.78rem;margin-top:0.3rem">See how your ATS & match scores improve over time</div>
</div>

<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:1rem;text-align:center">
  <div style="font-size:1.5rem;margin-bottom:0.4rem"></div>
  <div style="color:#e2e8f0;font-size:0.82rem;font-weight:600">Skill Gap Chart</div>
  <div style="color:#64748b;font-size:0.78rem;margin-top:0.3rem">Top skills you keep missing across all jobs</div>
</div>

<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:1rem;text-align:center">
  <div style="font-size:1.5rem;margin-bottom:0.4rem"></div>
  <div style="color:#e2e8f0;font-size:0.82rem;font-weight:600">Analysis History</div>
  <div style="color:#64748b;font-size:0.78rem;margin-top:0.3rem">Full log of every resume + job you've analyzed</div>
</div>
</div>

<div style="background:rgba(96,165,250,0.07);border:1px solid rgba(96,165,250,0.2);border-radius:10px;padding:0.9rem;font-size:0.85rem;color:#93c5fd">
<strong>How to use it:</strong> Analyze your resume against 5+ different jobs → come back here → you'll see which skills keep appearing in your "missing"list → those are the skills to learn next!
</div>
</div>
""", unsafe_allow_html=True)

    # ── FULL WORKFLOW ──
    st.markdown('<div class="section-title">The Complete Job Application Workflow</div>', unsafe_allow_html=True)
    st.markdown("""
<div style="background:linear-gradient(135deg,rgba(139,92,246,0.06),rgba(16,185,129,0.04));border:1px solid rgba(139,92,246,0.25);border-radius:16px;padding:2rem;margin-bottom:1.5rem">

<div style="display:flex;flex-direction:column;gap:0">

<div style="display:flex;gap:1rem;align-items:flex-start;padding:1rem 0;border-bottom:1px solid rgba(255,255,255,0.05)">
  <div style="width:36px;height:36px;border-radius:50%;background:rgba(139,92,246,0.2);border:1px solid rgba(139,92,246,0.4);display:flex;align-items:center;justify-content:center;font-family:Syne,sans-serif;font-weight:800;color:#a78bfa;flex-shrink:0;font-size:0.9rem">1</div>
  <div>
    <div style="font-weight:600;color:#e2e8f0;margin-bottom:0.2rem">Analyze your current resume against the target job</div>
    <div style="font-size:0.84rem;color:#64748b">Go to <strong style="color:#94a3b8">Analyzer</strong> → upload resume + paste job description → get your baseline score</div>
  </div>
</div>

<div style="display:flex;gap:1rem;align-items:flex-start;padding:1rem 0;border-bottom:1px solid rgba(255,255,255,0.05)">
  <div style="width:36px;height:36px;border-radius:50%;background:rgba(16,185,129,0.2);border:1px solid rgba(16,185,129,0.4);display:flex;align-items:center;justify-content:center;font-family:Syne,sans-serif;font-weight:800;color:#10b981;flex-shrink:0;font-size:0.9rem">2</div>
  <div>
    <div style="font-weight:600;color:#e2e8f0;margin-bottom:0.2rem">If ATS score is below 80% → Rewrite your resume</div>
    <div style="font-size:0.84rem;color:#64748b">Go to <strong style="color:#94a3b8">Resume Builder</strong> → Rewrite mode → paste resume + job description → download rewritten version</div>
  </div>
</div>

<div style="display:flex;gap:1rem;align-items:flex-start;padding:1rem 0;border-bottom:1px solid rgba(255,255,255,0.05)">
  <div style="width:36px;height:36px;border-radius:50%;background:rgba(139,92,246,0.2);border:1px solid rgba(139,92,246,0.4);display:flex;align-items:center;justify-content:center;font-family:Syne,sans-serif;font-weight:800;color:#a78bfa;flex-shrink:0;font-size:0.9rem">3</div>
  <div>
    <div style="font-weight:600;color:#e2e8f0;margin-bottom:0.2rem">Re-analyze the rewritten resume to verify 80+ ATS score</div>
    <div style="font-size:0.84rem;color:#64748b">Go back to <strong style="color:#94a3b8">Analyzer</strong> → paste rewritten resume → confirm score improved → repeat if needed</div>
  </div>
</div>

<div style="display:flex;gap:1rem;align-items:flex-start;padding:1rem 0;border-bottom:1px solid rgba(255,255,255,0.05)">
  <div style="width:36px;height:36px;border-radius:50%;background:rgba(245,158,11,0.2);border:1px solid rgba(245,158,11,0.4);display:flex;align-items:center;justify-content:center;font-family:Syne,sans-serif;font-weight:800;color:#f59e0b;flex-shrink:0;font-size:0.9rem">4</div>
  <div>
    <div style="font-weight:600;color:#e2e8f0;margin-bottom:0.2rem">Write your cover letter</div>
    <div style="font-size:0.84rem;color:#64748b">Go to <strong style="color:#94a3b8">Cover Letter</strong> → paste resume + job description → choose tone → generate → download</div>
  </div>
</div>

<div style="display:flex;gap:1rem;align-items:flex-start;padding:1rem 0;border-bottom:1px solid rgba(255,255,255,0.05)">
  <div style="width:36px;height:36px;border-radius:50%;background:rgba(239,68,68,0.2);border:1px solid rgba(239,68,68,0.4);display:flex;align-items:center;justify-content:center;font-family:Syne,sans-serif;font-weight:800;color:#ef4444;flex-shrink:0;font-size:0.9rem">5</div>
  <div>
    <div style="font-weight:600;color:#e2e8f0;margin-bottom:0.2rem">Apply for the job (resume + cover letter ready!)</div>
    <div style="font-size:0.84rem;color:#64748b">Copy resume into Word/Docs → format cleanly → save as PDF → submit with your cover letter</div>
  </div>
</div>

<div style="display:flex;gap:1rem;align-items:flex-start;padding:1rem 0">
  <div style="width:36px;height:36px;border-radius:50%;background:rgba(96,165,250,0.2);border:1px solid rgba(96,165,250,0.4);display:flex;align-items:center;justify-content:center;font-family:Syne,sans-serif;font-weight:800;color:#60a5fa;flex-shrink:0;font-size:0.9rem">6</div>
  <div>
    <div style="font-weight:600;color:#e2e8f0;margin-bottom:0.2rem">If you get an interview → Use Interview Prep</div>
    <div style="font-size:0.84rem;color:#64748b">Go to <strong style="color:#94a3b8">Interview Prep</strong> → paste resume + job description → generate questions → practice out loud 3 times each!</div>
  </div>
</div>

</div>
</div>
""", unsafe_allow_html=True)

    # ── FAQ ──
    st.markdown('<div class="section-title">Frequently Asked Questions</div>', unsafe_allow_html=True)

    faqs = [
        ("Is this really free?", "Yes! You only need a free OpenRouter API key (openrouter.ai/keys — no credit card). The app itself is free. The AI calls use your own key so you control the cost. With the free tier you get 200 requests/day — more than enough for daily job searching."),
        ("Is my resume data private?", "Yes. Your resume is sent directly to the AI API and never stored on any server. The only data saved locally (on your computer) is your analysis history in a SQLite database for the Dashboard. Your API key is only in your browser session and is never saved."),
        ("Why is my ATS score low?", "Low ATS scores usually mean: missing exact keywords from the job description, poor resume structure, or lack of quantified achievements. Use the 'Quick Wins'section in your analysis results — these are the fastest fixes. Then use the Rewrite tool to optimize."),
        ("What if I get a 404 or 429 error?", "404 = model was removed. Fix: switch to 'Auto Free Router'in sidebar. 429 = rate limit hit. Fix: wait 1 minute OR switch to a different provider (Groq has 14,400/day free). See the API Guide page for full error explanations."),
        ("Can I use this for any job type?", "Yes! It works for tech, business, healthcare, finance, marketing, and any other field. The AI adapts to whatever job description you paste. The more detailed your job description, the better the analysis."),
        ("How accurate is the ATS score?", "It's a realistic estimate based on real ATS logic (keyword matching, formatting, quantified achievements). It won't be 100% identical to every ATS system, but following its suggestions consistently improves callback rates. Treat scores above 75 as a green light to apply."),
        ("Should I use free or paid AI models?", "Free models (especially Llama 3.3 70B via Groq, or Auto Free Router via OpenRouter) give excellent results for resume analysis. Paid models like Claude 3.5 Sonnet give better writing quality for cover letters. Start free, upgrade if you want better cover letter writing."),
        ("How do I make my resume ATS-friendly?", "Key rules: Use exact keywords from the job description, quantify every achievement (numbers/%), use standard section headers (Experience, Education, Skills), avoid tables/images/columns, list your skills explicitly, and keep to 1-2 pages. This app tells you all of this automatically!"),
    ]

    for q, a in faqs:
        with st.expander(f"{q}"):
            st.markdown(f'<div style="color:#94a3b8;font-size:0.9rem;line-height:1.7;padding:0.5rem 0">{a}</div>', unsafe_allow_html=True)

    # ── QUICK TIPS ──
    st.markdown('<div class="section-title">Quick Tips for Best Results</div>', unsafe_allow_html=True)
    tips = [
        ("", "Always paste the FULL job description", "Don't just paste the title or bullet points — paste everything including requirements, responsibilities, and qualifications. More text = better keyword matching."),
        ("", "Analyze the SAME resume for multiple jobs", "Each job needs different keywords. Run the analyzer for each application and use the Rewrite tool to tailor your resume for every job separately."),
        ("", "Aim for ATS score 75+ before applying", "If your ATS score is below 75, the automated system will likely reject you before a human sees it. Use Quick Wins + Rewrite tool to get above 75."),
        ("", "Add numbers everywhere", "\"Led a team\"→ \"Led a team of 5\". \"Improved performance\"→ \"Improved performance by 40%\". Numbers make you 40% more likely to pass screening."),
        ("", "Mirror the job description language exactly", "If the job says 'data pipeline'use exactly that phrase — not 'data workflow'. ATS systems do exact keyword matching, not synonym matching."),
        ("", "Use the Dashboard to find skill gaps", "Analyze 10 jobs in your target field → check the Dashboard → the skills chart shows which skills appear most often across all your 'missing'lists — those are what to learn next!"),
    ]
    cols = st.columns(2)
    for i, (icon, title, desc) in enumerate(tips):
        with cols[i % 2]:
            st.markdown(f"""<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:1.1rem;margin-bottom:0.8rem">
<div style="display:flex;gap:0.7rem;align-items:flex-start">
  <div style="font-size:1.4rem;flex-shrink:0">{icon}</div>
  <div>
    <div style="font-weight:600;color:#e2e8f0;font-size:0.9rem;margin-bottom:0.3rem">{title}</div>
    <div style="font-size:0.82rem;color:#64748b;line-height:1.6">{desc}</div>
  </div>
</div>
</div>""", unsafe_allow_html=True)

    # ── READY CTA ──
    st.markdown("""<div style="background:linear-gradient(135deg,rgba(139,92,246,0.12),rgba(16,185,129,0.08));border:1px solid rgba(139,92,246,0.35);border-radius:16px;padding:2rem;text-align:center;margin-top:2rem">
<div style="font-family:Syne,sans-serif;font-size:1.4rem;font-weight:800;color:#e2e8f0;margin-bottom:0.6rem">Ready to Start?</div>
<div style="color:#94a3b8;font-size:0.9rem;margin-bottom:1.2rem">Get your free API key → come back → click <strong style="color:#e2e8f0">Analyzer</strong> in the sidebar</div>
<div style="display:flex;justify-content:center;gap:1rem;flex-wrap:wrap;font-size:0.85rem">
  <a href="https://openrouter.ai/keys"target="_blank"style="background:rgba(139,92,246,0.2);border:1px solid rgba(139,92,246,0.4);color:#a78bfa;padding:8px 20px;border-radius:10px;text-decoration:none;font-weight:700">Get OpenRouter Key (Free)</a>
  <a href="https://console.groq.com/keys"target="_blank"style="background:rgba(245,158,11,0.12);border:1px solid rgba(245,158,11,0.3);color:#fbbf24;padding:8px 20px;border-radius:10px;text-decoration:none;font-weight:700">Get Groq Key (Fastest)</a>
  <a href="https://aistudio.google.com/app/apikey"target="_blank"style="background:rgba(96,165,250,0.1);border:1px solid rgba(96,165,250,0.3);color:#93c5fd;padding:8px 20px;border-radius:10px;text-decoration:none;font-weight:700">Get Gemini Key (1M/day Free)</a>
</div>
</div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════
    st.markdown("""<div class="hero"><div class="hero-badge">Free · Open Source · For Every Job Seeker</div>
    <h1>About AI Career Suite</h1>
    <p>Built by a job seeker, for job seekers — because ATS systems reject 75% of resumes before a human ever sees them</p></div>""", unsafe_allow_html=True)
    st.markdown("""
### Tools
| Tool | What it does |
|------|-------------|
| **Resume Analyzer** | ATS score, job match, interview probability, red flags, salary insight |
| **Cover Letter** | Custom ATS-friendly cover letter in 15 seconds |
| **Interview Prep** | Role-specific Q&A based on YOUR resume |
| **Resume Builder** | Build from scratch OR rewrite existing resume for any job |
| **Dashboard** | Track progress and skill gaps across all applications |

---

### AI Models (30+ total)
**Free:** Gemma 4 31B (NVIDIA) · Auto Router · Llama 3.3 · DeepSeek R1 · Gemma 3 27B · Qwen3 Coder · OpenAI GPT-OSS 120B · Mistral · Nemotron · and 25+ more

**Paid:** Claude Sonnet/Opus · GPT-4o · Gemini 2.5 Pro · Grok 4 · DeepSeek R1

Get free key: [build.nvidia.com](https://build.nvidia.com) · [openrouter.ai/keys](https://openrouter.ai/keys)

---

### Tech Stack
Python 3.11 · NVIDIA NIM · OpenRouter API · SQLite · Streamlit · pdfplumber · Streamlit Cloud

---

### Privacy
Resume never stored on any server · Data only on your local machine · API key only in browser session

---

### Author
**Yagyesh Vyas** — Data & IT Developer | CS Graduate Student | F1 Visa

[LinkedIn](https://www.linkedin.com/in/yagyeshvyas) · [Portfolio](https://yagyesh-vyas-g11k379.gamma.site/) · [GitHub](https://github.com/yagyeshVyas)

If this helped you land a job, please star the repo!
    """)
