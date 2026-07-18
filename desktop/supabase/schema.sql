-- YanaNotes licensing schema.
-- Run this in the Supabase SQL editor once, then use email OTP for 2FA.
--
-- Model: every user who verifies their email gets a `licenses` row that
-- starts as 'pending'. The app stays locked until you (the admin) flip the
-- row to 'approved' -> manual approval of every licence.

create table if not exists public.licenses (
    id          uuid primary key default gen_random_uuid(),
    email       text unique not null,
    status      text not null default 'pending'
                check (status in ('pending', 'approved', 'revoked')),
    created_at  timestamptz not null default now(),
    approved_at timestamptz
);

-- Keep approved_at in step with status changes.
create or replace function public.touch_license_approval()
returns trigger language plpgsql as $$
begin
    if new.status = 'approved' and (old.status is distinct from 'approved') then
        new.approved_at := now();
    end if;
    return new;
end;
$$;

drop trigger if exists trg_touch_license_approval on public.licenses;
create trigger trg_touch_license_approval
    before update on public.licenses
    for each row execute function public.touch_license_approval();

-- Row level security: a signed in user may read and create ONLY their own
-- licence row (matched on the email in their JWT). They can never approve
-- themselves; only the service role / dashboard can change status.
alter table public.licenses enable row level security;

drop policy if exists "read own licence" on public.licenses;
create policy "read own licence" on public.licenses
    for select using (auth.jwt() ->> 'email' = email);

drop policy if exists "create own pending licence" on public.licenses;
create policy "create own pending licence" on public.licenses
    for insert with check (
        auth.jwt() ->> 'email' = email and status = 'pending'
    );

-- Convenience view for the admin: who is waiting for approval.
create or replace view public.pending_licenses as
    select email, created_at from public.licenses where status = 'pending'
    order by created_at;

-- To approve someone from the SQL editor:
--   update public.licenses set status = 'approved' where email = 'name@x.com';
-- To revoke:
--   update public.licenses set status = 'revoked' where email = 'name@x.com';
