from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from app.retriever import retrieve
from app.guardrails import is_blocked

app = FastAPI(title="SHL Assessment Recommender")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Request Models
# ----------------------------

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# ----------------------------
# Context Extraction
# ----------------------------

def extract_context(history):

    context = {
        "skills": [],
        "personality": False,
        "seniority": None
    }

    text = history.lower()

    # Personality detection
    if "personality" in text:
        context["personality"] = True

    # Seniority detection
    if "senior" in text:
        context["seniority"] = "senior"

    elif "mid" in text:
        context["seniority"] = "mid"

    elif "junior" in text:
        context["seniority"] = "junior"

    # Skills extraction
    skills = [
    "java",
    "python",
    "backend",
    "frontend",
    "leadership",
    "communication",
    "problem",
    "solving",
    "problem solving",
    "stakeholder",
    "developer",
    "manager",
    "reasoning",
    "aptitude",
    "software",
    "engineer",
    "coding",
    "technical",
    "teamwork",
    "sales",
    "personality",
    "cognitive"
]
    
    for s in skills:
        if s in text:
            context["skills"].append(s)

    return context


# ----------------------------
# Health Endpoint
# ----------------------------

@app.get("/health")
def health():
    return {"status": "ok"}


# ----------------------------
# Chat Endpoint
# ----------------------------

@app.post("/chat")
def chat(req: ChatRequest):

    # Full conversation history
    history = " ".join([
        f"{m.role}: {m.content}"
        for m in req.messages
    ])

    lower_history = history.lower()

    # ----------------------------
    # Guardrails
    # ----------------------------

    if is_blocked(history):
        return {
            "reply": "I can only help with SHL assessments and recommendations.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # ----------------------------
    # Clarification Logic
    # ----------------------------

    vague_queries = [
        "assessment",
        "test",
        "hiring",
        "candidate",
        "hi",
        "hello"
    ]

    if (
        len(history.split()) < 5
        or lower_history.strip() in vague_queries
    ):
        return {
            "reply": (
                "Could you share the role, experience level, "
                "and skills you want to assess?"
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # ----------------------------
    # Comparison Mode
    # ----------------------------

    if (
        "compare" in lower_history
        or "difference" in lower_history
        or (
            "opq" in lower_history
            and "verify" in lower_history
        )
    ):
        
        return {
            "reply": (
                "OPQ32r focuses on workplace personality, communication style, "
                "behavioral preferences, and leadership potential, while "
                "Verify Interactive G+ evaluates cognitive ability, reasoning, "
                "problem-solving, and aptitude skills."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # ----------------------------
    # Extract Context
    # ----------------------------

    context = extract_context(history)

    # Build semantic retrieval query
    query_parts = []

    query_parts.extend(context["skills"])

    if context["personality"]:
        query_parts.append("personality")

    if context["seniority"]:
        query_parts.append(context["seniority"])

    query = " ".join(query_parts)

    # fallback
    if not query.strip():
        query = history

    # ----------------------------
    # Retrieve Assessments
    # ----------------------------

    results = retrieve(query)

    # Remove duplicates
    unique_results = []
    seen = set()

    for r in results:

        if r["name"] not in seen:
            unique_results.append(r)
            seen.add(r["name"])

    results = unique_results[:5]

    # ----------------------------
    # Build Recommendations
    # ----------------------------

    recommendations = []

    for r in results:

        recommendations.append({
            "name": r["name"],
            "url": r["url"],
            "test_type": r.get("test_type", "A")
        })

    # ----------------------------
    # Generate Reply
    # ----------------------------

    reply = (
        f"Here are {len(recommendations)} SHL assessments "
        f"matching your requirements."
    )

    if context["personality"]:
        reply += " I also included personality-focused assessments."

    # ----------------------------
    # Final Response
    # ----------------------------

    return {
        "reply": reply,
        "recommendations": recommendations,
        "end_of_conversation": False
    }