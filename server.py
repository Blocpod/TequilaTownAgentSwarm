from __future__ import annotations

import logging
from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from agency_swarm.integrations.fastapi import run_fastapi
from swarm import create_agency
from tequilatown_ui.dashboard_state import dashboard_state
from tequilatown_ui.mission_routing import MissionRequest, route_mission
from tequilatown_ui.system_status import system_status

load_dotenv()

logging.basicConfig(level=logging.INFO)

ROOT = Path(__file__).resolve().parent
UI_DIR = ROOT / "tequilatown_ui" / "static"
ASSETS_DIR = ROOT / "assets"

app = run_fastapi(
    agencies={"tequilatown-agent-swarm": create_agency},
    port=8080,
    return_app=True,
    enable_logging=True,
    allowed_local_file_dirs=["./uploads"],
)

app.mount("/static", StaticFiles(directory=UI_DIR), name="static")
app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")


@app.get("/", include_in_schema=False)
@app.get("/dashboard", include_in_schema=False)
def dashboard() -> FileResponse:
    return FileResponse(UI_DIR / "index.html")


@app.get("/api/dashboard/state")
def get_dashboard_state() -> dict:
    return dashboard_state()


@app.get("/api/system/status")
def get_system_status() -> dict:
    return system_status()


@app.post("/api/missions/route")
def post_mission_route(mission: MissionRequest) -> dict:
    return route_mission(mission)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "system": "TequilaTown AgentSwarm"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080, reload=False)
