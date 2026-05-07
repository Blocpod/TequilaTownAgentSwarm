from tequilatown_ui.system_status import system_status


PROVIDER_KEYS = ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY")


def test_system_status_blocks_without_model_provider(monkeypatch):
    for key in PROVIDER_KEYS + ("APP_TOKEN",):
        monkeypatch.delenv(key, raising=False)

    status = system_status()

    assert status["level"] == "blocked"
    assert "model provider" in status["summary"].lower()
    assert status["routes"]["missionRouter"] == "/api/missions/route"


def test_system_status_warns_without_app_token(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.delenv("APP_TOKEN", raising=False)

    status = system_status()

    assert status["level"] == "warning"
    assert "APP_TOKEN" in status["summary"]


def test_system_status_ready_with_provider_and_token(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("APP_TOKEN", "test-token")

    status = system_status()

    assert status["level"] == "ready"
    model_check = next(check for check in status["checks"] if check["name"] == "Model Provider")
    assert model_check["configured"] is True
    assert "OPENAI_API_KEY" in model_check["configuredKeys"]
