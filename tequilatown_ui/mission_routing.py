from __future__ import annotations

from pydantic import BaseModel, Field


class MissionRequest(BaseModel):
    title: str = Field(..., min_length=2, max_length=140)
    description: str = Field(..., min_length=2, max_length=4000)
    missionType: str = Field(default="general", max_length=80)


KEYWORD_ROUTES = (
    ("Ticketing Agent", ("ticket", "admission", "tixr", "package", "group sale")),
    ("VIP Upsell Agent", ("vip", "reservation", "premium", "bottle service", "hosted")),
    ("Merch and Bottle Sales", ("merch", "bottle", "retail", "checkout", "bundle")),
    ("Passport and Missions", ("passport", "qr", "mission", "reward", "check-in", "checkin")),
    ("CRM and Lead Capture", ("crm", "lead", "profile", "consent", "preference")),
    ("AI Bartender", ("tequila", "cocktail", "tasting", "drink", "bartender")),
    ("AI Chef", ("food", "pairing", "menu", "allergy", "dietary")),
    ("Tour Guide", ("route", "wayfinding", "navigation", "room", "accessibility")),
    ("Cultural Storyteller", ("culture", "agave", "mexico", "story", "education")),
    ("Schedule Agent", ("schedule", "run of show", "staffing", "calendar", "timing")),
    ("Analytics Agent", ("analytics", "kpi", "dashboard", "report", "forecast")),
    ("Feedback Agent", ("survey", "feedback", "review", "sentiment", "complaint")),
    ("Sponsor Intelligence", ("sponsor", "partner", "activation", "roi", "recap")),
    ("Internal Ops Agent", ("ops", "sop", "incident", "handoff", "issue")),
    ("Research Agent", ("research", "trend", "competitor", "benchmark", "source")),
    ("Docs Agent", ("doc", "brief", "sop", "markdown", "pdf", "contract")),
    ("Slides Agent", ("slide", "deck", "ppt", "presentation", "pitch")),
    ("Image Agent", ("image", "visual", "creative", "ad", "photo")),
    ("Video Agent", ("video", "reel", "promo", "clip", "caption")),
)

TYPE_ROUTES = {
    "new mission": "Orchestrator",
    "new project": "Orchestrator",
    "upload brief": "Docs Agent",
    "swarm report": "Analytics Agent",
}


def route_mission(mission: MissionRequest) -> dict:
    text = f"{mission.title} {mission.description} {mission.missionType}".lower()
    selected = TYPE_ROUTES.get(mission.missionType.lower(), "Orchestrator")

    for agent, keywords in KEYWORD_ROUTES:
        if any(keyword in text for keyword in keywords):
            selected = agent
            break

    prompt = (
        f"Mission: {mission.title}\n"
        f"Type: {mission.missionType}\n\n"
        f"{mission.description.strip()}\n\n"
        "Route this through TequilaTown AgentSwarm, preserve brand voice, "
        "and return concrete next actions."
    )

    return {
        "status": "ready",
        "recommendedAgent": selected,
        "agencyEndpoint": "/tequilatown-agent-swarm/get_response",
        "streamEndpoint": "/tequilatown-agent-swarm/get_response_stream",
        "prompt": prompt,
        "nextSteps": [
            f"Send the mission to {selected}.",
            "Escalate to the Master Orchestrator when multiple specialists are needed.",
            "Use the stream endpoint for live dashboard mission execution once provider keys are configured.",
        ],
    }
