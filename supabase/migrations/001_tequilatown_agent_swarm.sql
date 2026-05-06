-- TequilaTown AgentSwarm starter schema.
-- Supabase note: as of April 2026, new public tables may not be exposed to the
-- Data API automatically. This migration enables RLS and grants baseline
-- table/sequence access; tighten policies before production.

create extension if not exists pgcrypto;

create table if not exists public.agent_events (
  id uuid primary key default gen_random_uuid(),
  agent_name text not null,
  event_type text not null,
  entity_type text,
  entity_id uuid,
  payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.guest_profiles (
  id uuid primary key default gen_random_uuid(),
  external_id text unique,
  full_name text,
  email text,
  phone text,
  consent_marketing boolean not null default false,
  consent_sponsor_share boolean not null default false,
  preferences jsonb not null default '{}'::jsonb,
  tags text[] not null default array[]::text[],
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.ticket_orders (
  id uuid primary key default gen_random_uuid(),
  guest_id uuid references public.guest_profiles(id) on delete set null,
  provider text not null default 'tixr',
  provider_order_id text,
  ticket_type text,
  status text not null default 'unknown',
  party_size integer,
  gross_amount numeric(12,2),
  purchased_at timestamptz,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.missions (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  description text,
  starts_at timestamptz,
  ends_at timestamptz,
  reward jsonb not null default '{}'::jsonb,
  rules jsonb not null default '{}'::jsonb,
  active boolean not null default true,
  created_at timestamptz not null default now()
);

create table if not exists public.mission_progress (
  id uuid primary key default gen_random_uuid(),
  mission_id uuid not null references public.missions(id) on delete cascade,
  guest_id uuid references public.guest_profiles(id) on delete cascade,
  status text not null default 'started',
  scans integer not null default 0,
  completed_at timestamptz,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  unique (mission_id, guest_id)
);

create table if not exists public.purchases (
  id uuid primary key default gen_random_uuid(),
  guest_id uuid references public.guest_profiles(id) on delete set null,
  channel text not null,
  product_type text not null,
  product_name text not null,
  sponsor_name text,
  quantity integer not null default 1,
  gross_amount numeric(12,2),
  metadata jsonb not null default '{}'::jsonb,
  purchased_at timestamptz not null default now()
);

create table if not exists public.feedback (
  id uuid primary key default gen_random_uuid(),
  guest_id uuid references public.guest_profiles(id) on delete set null,
  rating integer check (rating is null or rating between 1 and 5),
  sentiment numeric(4,3),
  category text,
  message text,
  severity text not null default 'normal',
  status text not null default 'open',
  owner text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.sponsors (
  id uuid primary key default gen_random_uuid(),
  name text not null unique,
  category text,
  contact_name text,
  contact_email text,
  objectives jsonb not null default '{}'::jsonb,
  active boolean not null default true,
  created_at timestamptz not null default now()
);

create table if not exists public.sponsor_activations (
  id uuid primary key default gen_random_uuid(),
  sponsor_id uuid not null references public.sponsors(id) on delete cascade,
  activation_name text not null,
  room_or_station text,
  impressions integer not null default 0,
  engagements integer not null default 0,
  lead_captures integer not null default 0,
  revenue numeric(12,2),
  metadata jsonb not null default '{}'::jsonb,
  measured_at timestamptz not null default now()
);

create table if not exists public.ops_issues (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  description text,
  severity text not null default 'normal',
  status text not null default 'open',
  owner text,
  location text,
  source_agent text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  resolved_at timestamptz
);

create table if not exists public.content_assets (
  id uuid primary key default gen_random_uuid(),
  asset_type text not null,
  title text not null,
  status text not null default 'draft',
  owner text,
  sponsor_id uuid references public.sponsors(id) on delete set null,
  file_url text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.schedule_blocks (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  block_type text not null,
  location text,
  owner text,
  starts_at timestamptz not null,
  ends_at timestamptz not null,
  status text not null default 'scheduled',
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  check (ends_at > starts_at)
);

alter table public.agent_events enable row level security;
alter table public.guest_profiles enable row level security;
alter table public.ticket_orders enable row level security;
alter table public.missions enable row level security;
alter table public.mission_progress enable row level security;
alter table public.purchases enable row level security;
alter table public.feedback enable row level security;
alter table public.sponsors enable row level security;
alter table public.sponsor_activations enable row level security;
alter table public.ops_issues enable row level security;
alter table public.content_assets enable row level security;
alter table public.schedule_blocks enable row level security;

grant usage on schema public to anon, authenticated;
grant select, insert, update on all tables in schema public to authenticated;
grant select on public.missions, public.sponsors, public.schedule_blocks to anon;
grant usage, select on all sequences in schema public to authenticated;

create policy "public can read active missions"
  on public.missions for select
  to anon, authenticated
  using (active = true);

create policy "public can read active sponsors"
  on public.sponsors for select
  to anon, authenticated
  using (active = true);

create policy "public can read scheduled blocks"
  on public.schedule_blocks for select
  to anon, authenticated
  using (status = 'scheduled');

create policy "authenticated staff can manage agent events"
  on public.agent_events for all
  to authenticated
  using (true)
  with check (true);

create policy "authenticated staff can manage guest profiles"
  on public.guest_profiles for all
  to authenticated
  using (true)
  with check (true);

create policy "authenticated staff can manage ticket orders"
  on public.ticket_orders for all
  to authenticated
  using (true)
  with check (true);

create policy "authenticated staff can manage mission progress"
  on public.mission_progress for all
  to authenticated
  using (true)
  with check (true);

create policy "authenticated staff can manage purchases"
  on public.purchases for all
  to authenticated
  using (true)
  with check (true);

create policy "authenticated staff can manage feedback"
  on public.feedback for all
  to authenticated
  using (true)
  with check (true);

create policy "authenticated staff can manage sponsors"
  on public.sponsors for all
  to authenticated
  using (true)
  with check (true);

create policy "authenticated staff can manage sponsor activations"
  on public.sponsor_activations for all
  to authenticated
  using (true)
  with check (true);

create policy "authenticated staff can manage ops issues"
  on public.ops_issues for all
  to authenticated
  using (true)
  with check (true);

create policy "authenticated staff can manage content assets"
  on public.content_assets for all
  to authenticated
  using (true)
  with check (true);

create policy "authenticated staff can manage schedule blocks"
  on public.schedule_blocks for all
  to authenticated
  using (true)
  with check (true);

create index if not exists idx_agent_events_agent_created on public.agent_events (agent_name, created_at desc);
create index if not exists idx_guest_profiles_email on public.guest_profiles (email);
create index if not exists idx_ticket_orders_guest on public.ticket_orders (guest_id);
create index if not exists idx_mission_progress_guest on public.mission_progress (guest_id);
create index if not exists idx_purchases_guest on public.purchases (guest_id);
create index if not exists idx_feedback_status_severity on public.feedback (status, severity);
create index if not exists idx_sponsor_activations_sponsor on public.sponsor_activations (sponsor_id, measured_at desc);
create index if not exists idx_ops_issues_status_severity on public.ops_issues (status, severity);
create index if not exists idx_schedule_blocks_starts_at on public.schedule_blocks (starts_at);
