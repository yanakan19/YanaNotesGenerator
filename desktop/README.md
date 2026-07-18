# YanaNotes Desktop

A clean, black themed desktop app for browsing the study notes produced by the
YanaNotesGenerator pipeline. Email login with a six digit code (2FA), a
manually approved licence via Supabase, a local repository of your notes
organised by module and week, and settings for appearance, repository
location, and phone access.

Built entirely in Python with PySide6 (Qt).

---

## Features

- **Email login + 6 digit 2FA** using Supabase email OTP.
- **Manual licence approval**: every new email lands as `pending`; the app
  unlocks only after you approve it in Supabase.
- **Local repository** of notes, browsed as Module -> Week -> notes, split
  into **Generated notes** and **Raw notes**.
- **In app viewer** for PDF (QtPdf) and markdown/text; anything else opens in
  your system app.
- **Settings**: Light / System / Dark theme (live), change repository location
  with a migration popup (duplicate, remove link, start fresh, or delete old
  files), Google Drive sync for phone access, and sign out.
- **Smooth transitions** throughout (animated cross fades and slides).
- **Windows installer** via PyInstaller + Inno Setup.

---

## 1. Prerequisites

- Python 3.10 or newer.
- A Supabase project (free tier is fine).

## 2. Install

```bash
cd desktop
python -m venv .venv
# Windows:  .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt
```

## 3. Configure Supabase

1. Create a project at https://supabase.com.
2. In the SQL editor, run the contents of `supabase/schema.sql`. This creates
   the `licenses` table, row level security, and a `pending_licenses` view.
3. Enable email OTP so a **numeric code** is sent (not just a magic link):
   - **Authentication -> Providers -> Email**: keep email enabled.
   - **Authentication -> Email Templates -> Magic Link / OTP**: make sure the
     template includes the token, e.g. `Your code is {{ .Token }}`. Supabase
     sends a 6 digit code as `{{ .Token }}`.
4. Copy your project URL and anon key from **Project Settings -> API**.
5. Create your env file:

   ```bash
   cp .env.example .env
   ```

   and fill in `SUPABASE_URL` and `SUPABASE_ANON_KEY`.

## 4. Run

```bash
python run.py
```

Sign in with your email, enter the 6 digit code, and you'll land on the
**Awaiting approval** screen. To approve yourself, run this in the Supabase
SQL editor:

```sql
update public.licenses set status = 'approved' where email = 'you@example.com';
```

Click **Check again** in the app and you're in. See who is waiting with:

```sql
select * from public.pending_licenses;
```

## 5. Point it at your notes

Open **Settings -> Repository -> Change** and choose the folder that contains
your module folders (for example the root of the YanaNotesGenerator repo, or a
copy of it). The library reads the same layout the pipeline writes:

```
<repository>/
  ES3C2/
    module.md
    Week 01/
      sources/            -> shown under "Raw notes"
      ES3C2_Week01_Notes.pdf   -> shown under "Generated notes"
      ES3C2_Week01_Notes.md
      ES3C2_Week01_Notes.tex
```

## 6. Phone access (Google Drive)

Simplest path today: put your repository folder inside your Google Drive
folder and let the Google Drive desktop client sync it, then read the notes in
the Google Drive mobile app. The toggle lives in **Settings -> Phone access**.
Native in app Drive sign in is scaffolded in `yananotes/integrations/gdrive.py`
and activates once you add Google Cloud OAuth credentials.

---

## Building the Windows installer

```bash
# From the desktop/ folder, with the venv active:
pyinstaller build/yananotes.spec        # -> dist/YanaNotes/
iscc build/installer.iss                 # -> YanaNotes-Setup.exe (needs Inno Setup)
```

`build/yananotes.spec` produces a one folder app; `build/installer.iss` packs
it into a signed style installer with Start Menu and optional desktop
shortcuts.

> Ship `.env` alongside the packaged app, or add a first run config dialog, so
> the installed build knows your Supabase project. The anon key is safe to
> distribute; RLS protects the data.

---

## Project layout

```
desktop/
  run.py                     dev entry point
  requirements.txt
  .env.example
  supabase/schema.sql        licences table + RLS + admin view
  build/
    yananotes.spec           PyInstaller
    installer.iss            Inno Setup
  yananotes/
    app.py                   QApplication bootstrap + theme
    config.py                deployment env + persisted user settings
    async_task.py            run blocking work off the UI thread
    theme/                   colour tokens, QSS, animations
    auth/                    Supabase client, email OTP, session keychain
    library/                 repository scanner + models
    integrations/gdrive.py   phone sync scaffold
    ui/
      main_window.py         shell: auth flow + sidebar + pages
      widgets.py             reusable neon widgets
      pages/                 login, otp, pending, library, viewer, settings
```
