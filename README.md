# AI Powered Career Plateform

An advanced AI-powered career development platform built with Python and Streamlit that helps users analyze resumes, match jobs, generate career roadmaps, create study plans, and build professional portfolios using multiple AI providers.

## Features

### AI Resume Analyzer
- ATS score analysis
- Resume vs Job Description matching
- Missing skills detection
- Recruiter-style feedback
- Resume improvement suggestions
- Interview probability estimation

### Multi-AI Provider Support
Supports 15+ AI providers including:
- OpenAI
- OpenRouter
- NVIDIA Build
- Google Gemini
- Anthropic Claude
- Groq
- DeepSeek
- Mistral
- Together AI
- HuggingFace
- Ollama
- LM Studio.

### Career Intelligence
- AI-generated career path recommendations
- Salary growth visualization
- Skill gap analysis
- Learning roadmap generation
- Personalized study guides

 ### Job Matching System
- Resume-to-job matching engine
- Skill overlap analysis
- Match score calculation
- Missing requirement detection
- Smart job recommendations

### Portfolio Builder
- GitHub profile analyzer
- Repository insights
- Programming language breakdown
- AI-generated portfolio website code

### Gamification System
- XP and badge system
- Daily streak tracking
- Achievement unlocks
- User leaderboard

### Authentication System
- Secure login/signup
- Role-based access
- SQLite database integration
- Password hashing

### Modern UI/UX
- Luxury dark UI
- Glassmorphism effects
- 3D animations
- Interactive Plotly charts
- Responsive Streamlit interface

### Tech Stack
- Frontend
   - Streamlit
   - HTML/CSS
   - Plotly
- Backend
  - Python
  - SQLite
- AI & APIs
  - OpenAI API
  - OpenRouter API
  - NVIDIA NIM
  - Google Gemini
  - Anthropic Claude
- Libraries Used
  - pandas
  - requests
  - pdfplumber
  - beautifulsoup4
  - plotly

```text
# Project Structure
AI-Career-Suite/

│ 

├── app.py                  # Main Streamlit application

├── analyzer.py             # Resume analysis engine

├── auth.py                 # Authentication system

├── career.py               # Career recommendation engine

├── database.py             # SQLite database operations

├── gamification.py         # XP and badges system

├── job_matching.py         # Job matching engine

├── learning.py             # Study guide generator

├── portfolio.py            # Portfolio builder

├── providers.py            # AI provider integrations

├── scrape_job.py           # Job scraping utility

├── requirements.txt        # Dependencies

└── README.md
```

## Installation

1️. Clone the Repository
git clone https://github.com/your-username/AI-Career-Suite.git
cd AI-Career-Suite

2️. Create Virtual Environment
Windows
python -m venv venv
venv\Scripts\activate
Mac/Linux
python3 -m venv venv
source venv/bin/activate

3️. Install Dependencies
pip install -r requirements.txt

# Run the Project
streamlit run app.py

# API Keys Setup
You can use:
- OpenRouter API Key
- OpenAI API Key
- NVIDIA Build API Key
- Gemini API Key
- Claude API Key

The platform supports both:
- Free AI models
- Paid AI models
API keys can be entered directly inside the application UI.

## Main Modules

### Resume Analyzer
Upload your resume PDF and compare it against a job description to receive:
- ATS score
- Match percentage
- Missing skills
- Recruiter feedback
- Improvement suggestions

### Career Recommendation Engine
Get:
- Personalized career paths
- Salary estimates
- Skill recommendations
- Career growth roadmap

### Learning Assistant
Generate:
- 4-week study plans
- Learning roadmaps
- Practical exercises
- Course recommendations

### Job Matching
The AI compares your resume with available jobs and calculates:
- Match score
- Matching skills
- Missing skills
- Best-fit jobs

### AI Portfolio Builder
Connect your GitHub profile to:
- Analyze repositories
- Detect programming languages
- Generate portfolio website code
- Showcase projects professionally

### Gamification Features
Users can unlock badges like:
- ATS Apprentice
- ATS Master
- Interview Ready
- Continuous Learner
- Web Artisan
- Streak Master

### Database Features
The SQLite database stores:
- Resume analyses
- User accounts
- XP and badges
- Job postings
- Application tracking
- User activities

### Smart Job Scraper
Supports scraping job descriptions from:
- LinkedIn
- Greenhouse
- Lever
- Company career pages

### Future Improvements
- AI interview simulator
- Voice-based mock interviews
- Resume builder
- AI networking assistant
- LinkedIn optimization tool
- Cloud deployment
- Real-time recruiter dashboard

### Why This Project is Advanced
-  Multi-AI Provider Architecture
-  ATS Resume Intelligence
-  Career Roadmap Generation
-  AI Study Planner
-  Job Recommendation Engine
-  GitHub Portfolio Analyzer
-  Gamification System
-  Authentication & Database
-  Modern 3D UI Design
-  Real-world Career Workflow Automation



# Fork the repository
# Create your feature branch
git checkout -b feature-name

# Commit your changes
git commit -m "Added new feature"

# Push to branch
git push origin feature-name

# License
This project is licensed under educationlal purpose.

# Author
Developed by Renugha .V
