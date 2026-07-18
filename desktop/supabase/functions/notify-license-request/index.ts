// Supabase Edge Function: email the admin when a new licence request lands.
//
// Trigger it from a Database Webhook on INSERT into public.licenses (see
// supabase/notify.sql for the one line setup). It emails you via Resend so
// you can approve the request. No app change is needed; approval is still the
// SQL update in schema.sql.
//
// Deploy:
//   supabase functions deploy notify-license-request
//   supabase secrets set RESEND_API_KEY=...  ADMIN_EMAIL=you@example.com \
//                        FROM_EMAIL="YanaNotes <notify@yourdomain>"

import { serve } from "https://deno.land/std@0.208.0/http/server.ts";

interface WebhookPayload {
  type: string;
  table: string;
  record: { email?: string; status?: string; created_at?: string } | null;
}

serve(async (req) => {
  try {
    const payload = (await req.json()) as WebhookPayload;
    const record = payload.record;
    if (!record?.email) {
      return new Response("ignored: no record", { status: 200 });
    }

    const resendKey = Deno.env.get("RESEND_API_KEY");
    const adminEmail = Deno.env.get("ADMIN_EMAIL");
    const fromEmail = Deno.env.get("FROM_EMAIL") ?? "YanaNotes <onboarding@resend.dev>";
    if (!resendKey || !adminEmail) {
      return new Response("missing RESEND_API_KEY or ADMIN_EMAIL", { status: 500 });
    }

    const body = {
      from: fromEmail,
      to: [adminEmail],
      subject: `YanaNotes licence request: ${record.email}`,
      text:
        `A new YanaNotes licence request is waiting for approval.\n\n` +
        `Email: ${record.email}\n` +
        `Requested: ${record.created_at ?? "just now"}\n\n` +
        `Approve it in the Supabase SQL editor:\n` +
        `  update public.licenses set status = 'approved' ` +
        `where email = '${record.email}';\n`,
    };

    const res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${resendKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      return new Response(`resend error: ${await res.text()}`, { status: 502 });
    }
    return new Response("notified", { status: 200 });
  } catch (err) {
    return new Response(`error: ${err}`, { status: 500 });
  }
});
