from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class IntegrationCheck:
    name: str
    keys: tuple[str, ...]
    required: bool = False


PROVIDER_KEYS = ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY")

INTEGRATIONS = (
    IntegrationCheck("Model Provider", PROVIDER_KEYS, required=True),
    IntegrationCheck("Dashboard/API Token", ("APP_TOKEN",), required=False),
    IntegrationCheck("Composio", ("COMPOSIO_API_KEY", "COMPOSIO_USER_ID")),
    IntegrationCheck("Supabase", ("SUPABASE_URL", "SUPABASE_ANON_KEY")),
    IntegrationCheck("Supabase Service Role", ("SUPABASE_SERVICE_ROLE_KEY",)),
    IntegrationCheck("Search API", ("SEARCH_API_KEY",)),
    IntegrationCheck("Fal.ai", ("FAL_KEY",)),
    IntegrationCheck("Pexels", ("PEXELS_API_KEY",)),
    IntegrationCheck("Pixabay", ("PIXABAY_API_KEY",)),
    IntegrationCheck("Unsplash", ("UNSPLASH_ACCESS_KEY",)),
)


def _is_set(name: str) -> bool:
    return bool(os.getenv(name, "").strip())


def system_status() -> dict:
    checks = []
    for item in INTEGRATIONS:
        configured = [key for key in item.keys if _is_set(key)]
        complete = bool(configured) if item.keys == PROVIDER_KEYS else len(configured) == len(item.keys)
        checks.append(
            {
                "name": item.name,
                "required": item.required,
                "configured": complete,
                "configuredKeys": configured,
                "missingKeys": [key for key in item.keys if key not in configured],
            }
        )

    provider_ready = any(_is_set(key) for key in PROVIDER_KEYS)
    app_token_ready = _is_set("APP_TOKEN")
    required_ready = provider_ready

    if required_ready and app_token_ready:
        level = "ready"
        summary = "Ready for authenticated agent runs."
    elif required_ready:
        level = "warning"
        summary = "Model provider is configured; APP_TOKEN is not set, so local API auth is disabled."
    else:
        level = "blocked"
        summary = "Add at least one model provider key before running live agent missions."

    return {
        "level": level,
        "summary": summary,
        "defaultModel": os.getenv("DEFAULT_MODEL", "gpt-5.2"),
        "checks": checks,
        "routes": {
            "dashboard": "/",
            "state": "/api/dashboard/state",
            "missionRouter": "/api/missions/route",
            "agencyMetadata": "/tequilatown-agent-swarm/get_metadata",
            "agencyResponse": "/tequilatown-agent-swarm/get_response",
            "agencyStream": "/tequilatown-agent-swarm/get_response_stream",
        },
    }
