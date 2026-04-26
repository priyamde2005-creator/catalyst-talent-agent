import os
import json
import re
from groq import Groq
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Catalyst Talent Scouting Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

with open("candidates.json", "r") as f:
    CANDIDATES = json.load(f)

class JDRequest(BaseModel):
    job_description: str

def ask_ai(prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1000,
    )
    return response.choices[0].message.content.strip()

def clean_json(raw: str) -> dict:
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"^```\s*", "", raw)
    raw = re.sub(r"```$", "", raw).strip()
    return json.loads(raw)

def parse_jd(jd_text: str) -> dict:
    prompt = f"""Parse this job description and return ONLY a JSON object with these fields:
- role_title: job title
- required_skills: list of required skills
- preferred_skills: list of preferred/nice-to-have skills
- min_experience: minimum years of experience (number)
- max_experience: maximum years of experience (number, use 99 if not specified)
- location: preferred location or "Any"
- role_type: one of [ML Engineer, Data Scientist, Backend Engineer, Frontend Engineer, Full Stack, DevOps, Data Engineer, Product Manager, Designer, Other]
- key_requirements: list of 3-5 key requirements in plain English

Return ONLY valid JSON, no markdown, no explanation.

Job Description:
{jd_text}"""
    return clean_json(ask_ai(prompt))

def calculate_match_score(candidate: dict, jd: dict) -> dict:
    prompt = f"""You are a technical recruiter. Score this candidate against the job requirements.

JOB REQUIREMENTS:
{json.dumps(jd, indent=2)}

CANDIDATE PROFILE:
{json.dumps(candidate, indent=2)}

Return ONLY a JSON object with:
- match_score: number from 0-100
- skill_match: number from 0-100
- experience_match: number from 0-100
- match_reasons: list of 2-3 reasons why they match
- gap_reasons: list of 1-2 skill gaps or concerns

Return ONLY valid JSON, no markdown."""
    return clean_json(ask_ai(prompt))

def simulate_conversation(candidate: dict, jd: dict) -> dict:
    prompt = f"""Simulate a brief recruiter outreach conversation.

JOB ROLE: {jd.get('role_title', 'Software Engineer')}
CANDIDATE: {candidate['name']}, {candidate['current_role']} at {candidate['current_company']}
OPEN TO WORK: {candidate.get('open_to_work', True)}

Return ONLY a JSON object with:
- conversation: list of 3 objects with "speaker" (Recruiter/Candidate) and "message" fields
- interest_score: number 0-100
- interest_level: one of [High, Medium, Low, Not Interested]
- interest_reasoning: one sentence

Return ONLY valid JSON, no markdown."""
    return clean_json(ask_ai(prompt))

@app.get("/")
def root():
    return {"message": "Catalyst Talent Scouting Agent API", "status": "running"}

@app.post("/analyze")
def analyze_jd(request: JDRequest):
    if len(request.job_description.strip()) < 50:
        raise HTTPException(status_code=400, detail="Job description too short.")

    try:
        jd_summary = parse_jd(request.job_description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse JD: {str(e)}")

    scored_candidates = []
    for candidate in CANDIDATES:
        try:
            match_data = calculate_match_score(candidate, jd_summary)
            candidate_result = {
                **candidate,
                "match_score": match_data.get("match_score", 0),
                "skill_match": match_data.get("skill_match", 0),
                "experience_match": match_data.get("experience_match", 0),
                "match_reasons": match_data.get("match_reasons", []),
                "gap_reasons": match_data.get("gap_reasons", []),
            }
            scored_candidates.append(candidate_result)
        except Exception:
            continue

    scored_candidates.sort(key=lambda x: x["match_score"], reverse=True)
    top_candidates = scored_candidates[:5]

    final_candidates = []
    for candidate in top_candidates:
        try:
            conv_data = simulate_conversation(candidate, jd_summary)
            candidate["conversation"] = conv_data.get("conversation", [])
            candidate["interest_score"] = conv_data.get("interest_score", 50)
            candidate["interest_level"] = conv_data.get("interest_level", "Medium")
            candidate["interest_reasoning"] = conv_data.get("interest_reasoning", "")
            candidate["combined_score"] = round(0.6 * candidate["match_score"] + 0.4 * candidate["interest_score"])
        except Exception:
            candidate["conversation"] = []
            candidate["interest_score"] = 50
            candidate["interest_level"] = "Medium"
            candidate["interest_reasoning"] = "Could not assess"
            candidate["combined_score"] = round(0.6 * candidate["match_score"])
        final_candidates.append(candidate)

    final_candidates.sort(key=lambda x: x["combined_score"], reverse=True)
    for i, c in enumerate(final_candidates):
        c["rank"] = i + 1

    return {
        "jd_summary": jd_summary,
        "total_candidates_evaluated": len(CANDIDATES),
        "shortlisted": len(final_candidates),
        "candidates": final_candidates
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
