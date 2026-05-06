import os
from dotenv import load_dotenv
from agents import set_tracing_disabled, set_tracing_export_api_key
from patches.patch_agency_swarm_dual_comms import apply_dual_comms_patch
from patches.patch_file_attachment_refs import apply_file_attachment_reference_patch
from patches.patch_ipython_interpreter_composio import apply_ipython_composio_context_patch
from patches.patch_utf8_file_reads import apply_utf8_file_read_patch

load_dotenv()

apply_utf8_file_read_patch()
apply_dual_comms_patch()
apply_file_attachment_reference_patch()
apply_ipython_composio_context_patch()

_tracing_key = os.getenv("OPENAI_API_KEY")
if _tracing_key:
    set_tracing_export_api_key(_tracing_key)
else:
    set_tracing_disabled(True)


def create_agency(load_threads_callback=None):
    from agency_swarm import Agency
    from agency_swarm.tools import Handoff, SendMessage

    from orchestrator import create_orchestrator
    from virtual_assistant import create_virtual_assistant
    from deep_research import create_deep_research
    from data_analyst_agent import create_data_analyst
    from slides_agent import create_slides_agent
    from docs_agent import create_docs_agent
    from video_generation_agent import create_video_generation_agent
    from image_generation_agent import create_image_generation_agent
    from ai_bartender import create_ai_bartender
    from ai_chef import create_ai_chef
    from tour_guide import create_tour_guide
    from cultural_storyteller import create_cultural_storyteller
    from ticketing_agent import create_ticketing_agent
    from merch_bottle_sales_agent import create_merch_bottle_sales_agent
    from passport_missions_agent import create_passport_missions_agent
    from crm_lead_capture_agent import create_crm_lead_capture_agent
    from vip_upsell_agent import create_vip_upsell_agent
    from schedule_agent import create_schedule_agent
    from feedback_agent import create_feedback_agent
    from sponsor_intelligence_agent import create_sponsor_intelligence_agent
    from internal_ops_agent import create_internal_ops_agent

    orchestrator = create_orchestrator()
    guest_concierge = create_virtual_assistant()
    ai_bartender = create_ai_bartender()
    ai_chef = create_ai_chef()
    tour_guide = create_tour_guide()
    cultural_storyteller = create_cultural_storyteller()
    ticketing_agent = create_ticketing_agent()
    merch_bottle_sales_agent = create_merch_bottle_sales_agent()
    passport_missions_agent = create_passport_missions_agent()
    crm_lead_capture_agent = create_crm_lead_capture_agent()
    vip_upsell_agent = create_vip_upsell_agent()
    schedule_agent = create_schedule_agent()
    data_analyst = create_data_analyst()
    feedback_agent = create_feedback_agent()
    sponsor_intelligence_agent = create_sponsor_intelligence_agent()
    internal_ops_agent = create_internal_ops_agent()
    deep_research = create_deep_research()
    slides_agent = create_slides_agent()
    docs_agent = create_docs_agent()
    video_generation_agent = create_video_generation_agent()
    image_generation_agent = create_image_generation_agent()

    all_agents = [
        orchestrator,
        guest_concierge,
        ai_bartender,
        ai_chef,
        tour_guide,
        cultural_storyteller,
        ticketing_agent,
        merch_bottle_sales_agent,
        passport_missions_agent,
        crm_lead_capture_agent,
        vip_upsell_agent,
        schedule_agent,
        data_analyst,
        feedback_agent,
        sponsor_intelligence_agent,
        internal_ops_agent,
        deep_research,
        docs_agent,
        slides_agent,
        video_generation_agent,
        image_generation_agent,
    ]

    send_message_flows = [
        (orchestrator, specialist, SendMessage)
        for specialist in all_agents
        if specialist is not orchestrator
    ]

    handoff_flows = [
        (a > b, Handoff)
        for a in all_agents
        for b in all_agents
        if a is not b
    ]

    agency = Agency(
        *all_agents,
        communication_flows=send_message_flows + handoff_flows,
        name="TequilaTown AgentSwarm",
        shared_instructions="shared_instructions.md",
        load_threads_callback=load_threads_callback,
    )

    return agency

if __name__ == "__main__":
    agency = create_agency()
    agency.tui(show_reasoning=True, reload=False)
