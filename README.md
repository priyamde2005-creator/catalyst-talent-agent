# Catalyst — AI-Powered Talent Scouting & Engagement Agent

> Built for Catalyst Hackathon by Deccan AI

## 🚀 Live Demo
**Live App:** https://priyamde2005-creator.github.io/catalyst-talent-agent/frontend/

**Backend API:** https://catalyst-talent-agent.onrender.com

## 🎯 What It Does

Catalyst is an AI agent that automates talent scouting end-to-end:

1. **JD Parsing** — Paste any job description. AI extracts skills, experience, role type, and requirements automatically.
2. **Candidate Discovery & Matching** — Evaluates 20 candidate profiles and scores each on fit with full explainability.
3. **Conversational Engagement** — Simulates realistic 3-message recruiter ↔ candidate conversations to gauge genuine interest.
4. **Ranked Shortlist** — Outputs top 5 candidates ranked by combined score with match reasons, gaps, and conversation logs.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     RECRUITER                                    │
│                  Pastes Job Description                          │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                  FRONTEND (index.html)                           │
│         Dashboard UI · Score Display · Conversation Viewer       │
└───────────────────────┬─────────────────────────────────────────┘
                        │ POST /analyze
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│               FastAPI Backend (Python)                           │
│                                                                  │
│  ┌─────────────┐   ┌──────────────┐   ┌────────────────────┐   │
│  │  JD Parser  │──▶│ Match Engine │──▶│  Conv Simulator    │   │
│  │             │   │              │   │                    │   │
│  │ Extracts:   │   │ Scores all   │   │ Simulates 3-msg    │   │
│  │ • Skills    │   │ 20 candidates│   │ recruiter chat     │   │
│  │ • Exp years │   │ Match Score  │   │ Interest Score     │   │
│  │ • Role type │   │   (0–100)    │   │    (0–100)         │   │
│  └─────────────┘   └──────────────┘   └────────────────────┘   │
│         │                 │                    │                 │
│         └─────────────────┴────────────────────┘                │
│                           │                                      │
│                    ┌──────▼──────┐                               │
│                    │   Ranker    │                               │
│                    │ 0.6×Match + │                               │
│                    │ 0.4×Interest│                               │
│                    └─────────────┘                               │
│                                                                  │
│         All AI calls → Groq API (llama-3.3-70b-versatile)       │
│         Candidate data → candidates.json (20 profiles)          │
└───────────────────────┬─────────────────────────────────────────┘
                        │ Ranked shortlist (JSON)
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OUTPUT TO RECRUITER                           │
│     Top 5 candidates · Match + Interest + Combined scores        │
│     Match reasons · Skill gaps · Simulated conversation          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Scoring Logic

### Match Score (0–100)
Calculated by AI based on:
- Skill overlap with JD required/preferred skills
- Years of experience vs. requirements
- Role type alignment
- Education and background fit

### Interest Score (0–100)
Simulated by AI via a 3-message conversation:
- Recruiter reaches out about the role
- Candidate responds based on their profile
- Interest scored on enthusiasm, availability, and engagement

### Combined Score (Final Ranking)
```
Combined Score = 0.6 × Match Score + 0.4 × Interest Score
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| AI Model | Groq API — llama-3.3-70b-versatile (Free) |
| Backend | Python + FastAPI + Uvicorn |
| Frontend | Vanilla HTML / CSS / JavaScript |
| Candidate Data | Synthetic JSON (20 Indian tech profiles) |
| Deployment | Render.com (Free tier) |

---

## 🚀 Local Setup

### Prerequisites
- Python 3.10+
- Groq API Key (free at https://console.groq.com)

### Step 1 — Clone the repo
```bash
git clone https://github.com/priyamde2005-creator/catalyst-talent-agent
cd catalyst-talent-agent
```

### Step 2 — Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 3 — Set API key

**Windows:**
```cmd
set GROQ_API_KEY=your_groq_key_here
```

**Mac/Linux:**
```bash
export GROQ_API_KEY=your_groq_key_here
```

### Step 4 — Run backend
```bash
python main.py
```
Backend runs at: http://localhost:8000

### Step 5 — Open frontend
Open `frontend/index.html` in your browser.

---

## 📁 Project Structure

```
catalyst-talent-agent/
├── backend/
│   ├── main.py              # FastAPI app — all AI logic
│   ├── candidates.json      # 20 synthetic candidate profiles
│   └── requirements.txt     # Python dependencies
├── frontend/
│   └── index.html           # Complete recruiter dashboard UI
├── architecture.html        # System architecture diagram
└── README.md
```

---

## 🧪 Sample Input

```
We are looking for a Senior ML Engineer with 4-7 years of experience.

Required: Python, PyTorch, NLP, Transformer models, FastAPI, AWS
Preferred: LLM experience, MLOps, vector databases

Responsibilities: Build NLP models, deploy to production, mentor juniors
Location: Bangalore (Hybrid)
Salary: 20-35 LPA
```

## 📤 Sample Output

| Rank | Candidate | Role | Match | Interest | Combined |
|------|-----------|------|-------|----------|----------|
| #1 | Riya Chatterjee | NLP Engineer @ Freshworks | 92 | 88 | 91 |
| #2 | Ananya Ghosh | ML Engineer @ Flipkart | 87 | 79 | 84 |
| #3 | Arjun Sharma | Sr. SWE @ Infosys | 80 | 70 | 76 |
| #4 | Nikhil Bose | AI Researcher @ Samsung | 75 | 30 | 57 |
| #5 | Aditya Singh | Tech Lead @ Genpact | 70 | 65 | 68 |

Each result includes:
- ✅ Why they match (2-3 reasons)
- ⚠️ Skill gaps / concerns
- 💬 Full simulated conversation
- 👤 Complete candidate profile

---

## 👥 Team

Built by **Priyam De** for Catalyst Hackathon — Deccan AI 2026
