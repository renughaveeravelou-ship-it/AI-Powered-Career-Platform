# 🚀 AI Career Suite 2.0 — Dark Luxury 3D Edition

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/15+_AI_Providers-Supported-8b5cf6?style=for-the-badge" />
  <img src="https://img.shields.io/badge/NVIDIA_NIM-Gemma_4_31B-76b900?style=for-the-badge&logo=nvidia&logoColor=white" />
  <img src="https://img.shields.io/badge/100+_Models-Free_%26_Paid-10b981?style=for-the-badge" />
  <img src="https://img.shields.io/badge/UI_UX-3D_Glassmorphism-ec4899?style=for-the-badge" />
</p>

<p align="center">
  <strong>The world's most powerful open-source AI career assistant.</strong><br/>
  Interactive Copilot · Smart URL Scraper · 3D Analytics · Luxury Dark UI<br/>
  Works with 15+ AI providers including NVIDIA Build, OpenRouter, Groq, Google Gemini — and local models via Ollama.
</p>

<p align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHBkZnE4Z3JzMmRnbTV4Z2JzMmRnbTV4Z2JzMmRnbTV4Z2JzMmRnbTV4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKMGpxU88h8nK7u/giphy.gif" alt="AI Career Suite Demo" width="800">
</p>

<p align="center">
  <a href="https://ai-career-suite.streamlit.app/"><strong>🔗 Live Demo</strong></a> ·
  <a href="#-quick-start"><strong>⚡ Quick Start</strong></a> ·
  <a href="#-ai-providers--models"><strong>🤖 AI Providers</strong></a> ·
  <a href="#-new-features-in-v20"><strong>✨ v2.0 Features</strong></a>
</p>

---

## ✨ New Features in v2.0

### 🤖 1. AI Career Copilot (Interactive Chat)
A persistent, context-aware chatbot that acts as your elite executive coach.
- **Context-Aware**: Directly reads your last resume analysis and job target.
- **Dynamic Helper**: Ask it to rewrite specific lines, roleplay interviews, or suggest networking messages.
- **Direct Input**: Upload PDFs or scrape URLs directly inside the chat to give the AI context.

### 🕸️ 2. Smart URL Job Scraper
Stop copying and pasting! v2.0 introduces a BeautifulSoup-powered scraper.
- Just paste a job link from **Greenhouse, Lever, LinkedIn**, or company career pages.
- The app automatically extracts the job requirements and responsibilities for analysis.

### 📊 3. 3D Plotly Visualizations
We replaced static charts with interactive, glowing data visualizations.
- **Skill Radar Chart**: A 3D "Spider Web" plot visualizing your top missing skills.
- **Area Depth Chart**: Track your progress over time with layered, gradient area charts.

### 🎨 4. Ultra-Modern 3D UI
- **3D Tilt Hover**: Modules and cards physically tilt in 3D space as you hover.
- **Aurora Background**: Stunning, animated glassmorphism gradients.
- **Staggered Animations**: Content flows into the screen with cinematic precision.

---

## 🛠️ Core Tools

### 🎯 1. Resume Analyzer
Paste your resume + a job description. Get a full ATS-style recruiter analysis in ~15 seconds.

| Output | What it tells you |
|--------|-------------------|
| **ATS Score** (0–100) | How automated screening software rates your resume |
| **Job Match %** | How well your overall experience fits the role |
| **Interview Probability** | Realistic callback chance using real recruiter logic |
| **Matched Skills** | Keywords in both your resume and the JD |
| **Missing Skills** | Critical JD keywords completely absent from your resume |
| **Red Flags** | What a recruiter notices negatively in the first 6 seconds |
| **Quick Wins** | 3 things to fix TODAY that immediately improve callback rate |
| **Salary Insight** | Estimated market value based on your resume's positioning |
| **Strengths** | Genuine positives backed by evidence from your resume |
| **Improvements** | Specific rewording suggestions — not vague advice |

---

### ✉️ 2. Cover Letter Generator
Generates a fully custom, ATS-optimized cover letter tailored to the exact job.

- Starts with a strong hook — not *"I am writing to apply"*
- Uses YOUR actual achievements from your resume
- Injects 5 exact ATS keywords from the job description
- 3 tone options: Very Formal · Professional · Enthusiastic
- ~380 words, 3–4 paragraphs — exactly the right length

---

### 🎤 3. Interview Prep Guide
Generates role-specific questions based on YOUR resume — not generic answers from Google.

Each question includes:
- ❓ **The question** — specific to your own projects and experience
- 🎯 **Why they ask it** — so you understand the interviewer's intent
- ✅ **Ideal answer framework** — 3–4 bullets using your actual resume content
- ❌ **Common mistake to avoid**

Supports: Technical · Behavioral · Situational · Company Fit — 2–5 questions per category.

---

### 📝 4. AI Resume Builder — 2 Modes

**✨ Mode 1: Build Fresh Resume**
Fill in your details → AI builds a complete ATS-optimized resume from scratch.
Best for: students, career changers, writing your first resume.

**🔄 Mode 2: Rewrite for a Specific Job**
Paste your current resume + a target JD → AI rewrites the entire resume for that exact role.

Three rewrite options:
- 🔥 **Aggressive ATS Optimization** — injects exact JD keywords, mirrors language
- 📊 **Add Estimated Metrics** — adds realistic numbers/% where achievements lack them
- ✨ **Modernize Language** — replaces weak verbs (helped, worked) with power verbs (Engineered, Architected)

Download both the original and rewritten versions side-by-side to compare.

---

### 📊 5. Progress Dashboard
Track your entire job search across all analyses.

- **Score Trend Chart** — see ATS + match scores improving over time
- **Skill Gap Chart** — top missing skills across ALL your applications = your learning roadmap
- **Full History** — every resume + job analyzed, with matched/missing skill chips
- Delete any entry anytime

---

## 🤖 AI Providers & Models

The app supports **13 AI providers** and **70+ models** via a universal dispatcher (`providers.py`). Switch providers in the sidebar — everything else stays the same.

### 🆓 Free Providers — No Credit Card Needed

| Provider | Free Limits | Best Free Model | Get Key |
|----------|------------|-----------------|---------|
| 🟢 **NVIDIA Build** ⭐ | 1000 free credits | Gemma 4 31B IT | [build.nvidia.com](https://build.nvidia.com/explore/discover) |
| 🔀 **OpenRouter** | 20 req/min · 200/day | 🎲 Auto Free Router | [openrouter.ai/keys](https://openrouter.ai/keys) |
| ⚡ **Groq** | 30 req/min · 14,400/day | Llama 3.3 70B | [console.groq.com](https://console.groq.com/keys) |
| 🌙 **Google Gemini** | 15 req/min · 1M tokens/day | Gemini 2.0 Flash | [aistudio.google.com](https://aistudio.google.com/app/apikey) |
| 🤗 **Hugging Face** | Rate limited | Llama 3.1 8B | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) |
| 🌊 **Cohere** | 20/min · 1,000/month | Command R | [dashboard.cohere.com](https://dashboard.cohere.com/api-keys) |
| 🖥️ **Ollama (Local)** | Unlimited | Any model you pull | [ollama.com/download](https://ollama.com/download) |
| 🎨 **LM Studio (Local)** | Unlimited | Any GGUF file | [lmstudio.ai](https://lmstudio.ai) |

### 💳 Paid Providers (some have free signup credits)

| Provider | Free Credits | Best Model | Cost / Analysis* |
|----------|-------------|------------|-----------------|
| 🔥 **Together AI** | ✅ $25 free | Llama 3.3 70B Turbo | ~$0.002 |
| 🔥 **xAI Grok** | ✅ $25 free | Grok 3 Mini | ~$0.001 |
| 🧠 **DeepSeek** | ~$5 new acct | DeepSeek R1 | ~$0.001 |
| 💎 **OpenAI** | ~$5 new acct | GPT-4o Mini | ~$0.0006 |
| 👑 **Anthropic** | None | Claude 3.5 Sonnet | ~$0.008 |
| ⚡ **Mistral AI** | Trial credits | Mistral Small | ~$0.0002 |
| 🌐 **Perplexity** | None | Sonar (has web search) | ~$0.005 |

*\*Per analysis ≈ 2,000 input + 500 output tokens*

> **Best free setup:** NVIDIA Build (Gemma 4 31B) + OpenRouter (Auto Router) + Groq (Llama 3.3 70B). Three keys, 10 minutes total, unlimited free analyses.

---

## 🖥️ Local LLM — Ollama & LM Studio

Run AI entirely on your own machine. No API key. No cost. No data ever leaves your computer.

### Option A: Ollama (Recommended — command line)

```bash
# 1. Install from ollama.com/download

# 2. Pull a model (pick based on your RAM)
ollama pull llama3.2          # 2 GB  — good for 8 GB RAM laptops
ollama pull deepseek-r1:7b    # 4 GB  — best reasoning quality
ollama pull qwen2.5:14b       # 9 GB  — best quality for 16 GB RAM
ollama pull phi3.5            # 2 GB  — fastest on low-end hardware

# 3. Start the server
ollama serve

# 4. Run the app
streamlit run app.py
# Select 🖥️ Ollama (Local) in sidebar — no key needed
```

**RAM guide:**

| RAM | Recommended model |
|-----|------------------|
| 8 GB | `phi3.5` or `llama3.2` |
| 16 GB | `llama3.1` or `deepseek-r1:7b` |
| 32 GB+ | `qwen2.5:14b` or `deepseek-r1:14b` |
| NVIDIA GPU | Ollama auto-uses VRAM — much faster |

### Option B: LM Studio (GUI — drag & drop GGUF files)

1. Download from [lmstudio.ai](https://lmstudio.ai)
2. Search for any model inside LM Studio → Download — or drag-drop any `.gguf` file
3. Click **Local Server** tab → **Start Server**
4. In this app: select `🎨 LM Studio (Local)` → no key needed

> ⚠️ **Local LLMs only work when running the app locally** (`streamlit run app.py`).  
> They will NOT work on the Streamlit Cloud deployment — use any API provider for the deployed app.

---

## ⚡ Quick Start

### Option 1 — Use the Deployed App (Zero Setup)

1. Open → **[ai-career-suite.streamlit.app](https://ai-career-suite.streamlit.app/)**
2. Get a free API key → [openrouter.ai/keys](https://openrouter.ai/keys) (2 min, no card)
3. Paste key in sidebar → select **🎲 Auto Free Router**
4. Go to **🎯 Analyzer** → upload resume → paste JD → click Analyze

### Option 2 — Run Locally

```bash
# Clone the repo
git clone https://github.com/yagyeshVyas/ai-resume-analyzer.git
cd ai-resume-analyzer

# Install dependencies
pip install -r requirements.txt

# Run
streamlit run app.py
# Opens at http://localhost:8501
```

### Option 3 — Deploy Your Own Instance (Free)

1. Fork this repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub → select this repo → click **Deploy**
4. Live at `https://ai-career-suite.streamlit.app` in ~2 minutes

---

## 🔑 Get Your Free API Key (2 Minutes)

```
1. Go to: openrouter.ai/keys
2. Sign in with Google (free, no card)
3. Click "Create Key" → name it anything
4. Copy the key  (starts with sk-or-v1-)
5. Paste into the app sidebar
6. Select model: 🎲 Auto Free Router
```

The **Auto Free Router** (`openrouter/free`) automatically picks whichever free model has capacity — it never gives 404 or 429 errors.

---

## 📁 Project Structure

```
ai-resume-analyzer/
│
├── app.py              # Main Streamlit app — UI, sidebar, routing, all 5 tool pages
├── analyzer.py         # Resume analysis — prompt, JSON parsing, score clamping
├── providers.py        # Universal API dispatcher — all 12+ providers + error handling
├── database.py         # SQLite operations — save/retrieve/delete analyses
├── requirements.txt    # Python dependencies
└── README.md           # You're reading it
```

### Architecture — `providers.py`

Every tool makes a single call:

```python
result = call_api(provider_name, api_key, model_id, prompt)
```

The dispatcher handles all provider differences:

| Type | Providers |
|------|-----------|
| `openai_compat` | OpenRouter, NVIDIA Build, Groq, DeepSeek, Mistral, Together, Perplexity, xAI, LM Studio |
| `anthropic` | Anthropic Claude (different auth + response schema) |
| `gemini` | Google Gemini (URL-based key + nested response format) |
| `cohere` | Cohere (v2 chat endpoint) |
| `huggingface` | HuggingFace (model name in URL path) |
| `ollama` | Local Ollama server (health check + `/api/chat`) |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11 |
| UI Framework | Streamlit 1.32 |
| AI Providers | NVIDIA Build (NIM) · OpenRouter · OpenAI · Anthropic · Google Gemini · Groq · DeepSeek · Mistral · Together AI · Perplexity · xAI · Cohere · HuggingFace · Ollama · LM Studio |
| Database | SQLite (zero setup, local-only) |
| PDF Parsing | pdfplumber |
| Typography | Syne (headers) + DM Sans (body) via Google Fonts |
| Hosting | Streamlit Cloud (free tier) |

---

## 💡 Recommended Workflow

```
Step 1 → 🎯 Analyzer       Analyze resume vs job → get baseline ATS score
Step 2 → 📝 Resume Builder  Rewrite mode → rewrite for that specific job
Step 3 → 🎯 Analyzer        Re-analyze rewritten resume → verify 80+ ATS score
Step 4 → ✉️ Cover Letter    Generate custom cover letter
Step 5 → 📩 Apply           Submit resume PDF + cover letter
Step 6 → 🎤 Interview Prep  If you get an interview → practice questions out loud 3×
Step 7 → 📊 Dashboard       Review skill gaps → decide what to learn next
```

> Aim for **ATS score 75+** before applying. Below 75, most ATS systems reject you before a human ever reads your resume.

---

## 🔒 Privacy

- Resume text is sent **directly to your chosen AI API** — nowhere else
- Analysis history is saved **only on your local machine** in `analyses.db`
- Your API key lives only in your browser session — never logged, never stored
- Using Ollama or LM Studio? Your resume **never leaves your machine at all**

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss.

Ideas for contributions:
- New AI provider integrations
- Job board API integrations (LinkedIn, Indeed scraping)
- Resume template export (DOCX/PDF with formatting)
- Multi-language resume support
- Better JSON extraction for edge-case model outputs

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 👨‍💻 Author

**Yagyesh Vyas** — AI Engineer (Gen AI) 

Built this because I kept getting ghosted after applying and couldn't afford the paid tools. If it helps you land an interview, please ⭐ star the repo.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-yagyeshvyas-0077B5?style=flat&logo=linkedin)](https://www.linkedin.com/in/yagyeshvyas)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-8b5cf6?style=flat)](https://yagyesh-vyas-g11k379.gamma.site/)
[![GitHub](https://img.shields.io/badge/GitHub-yagyeshVyas-181717?style=flat&logo=github)](https://github.com/yagyeshVyas)

---

<p align="center">
  <strong>⭐ Star this repo if it helped you land a job or an interview!</strong>
</p>