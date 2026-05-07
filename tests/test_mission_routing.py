from tequilatown_ui.mission_routing import MissionRequest, route_mission


def test_routes_ticketing_mission_from_keywords():
    result = route_mission(
        MissionRequest(
            title="VIP birthday upsell",
            missionType="New Mission",
            description="Create a VIP ticket upsell mission for birthday groups.",
        )
    )

    assert result["status"] == "ready"
    assert result["recommendedAgent"] == "Ticketing Agent"
    assert result["streamEndpoint"] == "/tequilatown-agent-swarm/get_response_stream"
    assert "VIP birthday upsell" in result["prompt"]


def test_routes_docs_upload_brief_by_type():
    result = route_mission(
        MissionRequest(
            title="Upload brand brief",
            missionType="Upload Brief",
            description="Summarize this partner brief and extract tasks.",
        )
    )

    assert result["recommendedAgent"] == "Docs Agent"


def test_routes_sponsor_recap_to_analytics_before_slides():
    result = route_mission(
        MissionRequest(
            title="Sponsor recap deck",
            missionType="Swarm Report",
            description="Create a sponsor recap deck with guest flow and activation ROI.",
        )
    )

    assert result["recommendedAgent"] == "Analytics Agent"
