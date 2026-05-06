# TequilaTown AgentSwarm Customization Guide

This repo is a TequilaTown-branded clone of OpenSwarm. Keep the underlying OpenSwarm repository shape, Agency Swarm mechanics, shared tools, and file-generation agents intact unless a TequilaTown requirement truly needs a change.

## Product Shape

TequilaTown AgentSwarm is organized around four operating lanes:

- Guest Experience
- Commerce and Conversion
- Operations and Insights
- Creative Studio

The Master Orchestrator routes work. Specialists own execution.

## Editing Rules

- Preserve responsible alcohol, safety, privacy, consent, accessibility, and escalation guardrails.
- Keep agent instructions short enough to be operationally useful.
- Add new agents only when they own a distinct workflow.
- Update `swarm.py`, `shared_instructions.md`, `README.md`, and package file lists when adding or renaming agents.
- Keep only the canonical TequilaTown logo under `assets/tequilatown/logo.svg` unless the user explicitly asks to add more assets.
- Do not commit large raw video/media archives without Git LFS or external storage.
- Supabase schema changes should live under `supabase/migrations/` and must enable RLS for exposed tables.
