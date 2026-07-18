"""Google Drive sync integration (scaffold).

Phone access is achieved by keeping the repository folder mirrored to Google
Drive: enable the toggle in Settings, and the desktop app treats a Drive
backed folder like any other repository location, so the Drive mobile app
then surfaces the same notes on a phone.

Full OAuth device flow needs a Google Cloud project (client id / secret) and
is wired in a follow up once those credentials exist. The functions below
define the contract the Settings page already calls against so nothing else
has to change when the real client lands.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DriveStatus:
    available: bool
    connected: bool
    detail: str


def status() -> DriveStatus:
    """Report whether Drive sync can be used right now."""
    try:
        import google.auth  # noqa: F401  (presence check only)
    except Exception:
        return DriveStatus(
            available=False,
            connected=False,
            detail=(
                "Install the Google client libraries and add your Google "
                "Cloud OAuth credentials to enable phone sync."
            ),
        )
    return DriveStatus(
        available=True,
        connected=False,
        detail="Ready to connect. Sign in to Google to start syncing.",
    )


def guidance() -> str:
    """Human readable setup steps shown in Settings."""
    return (
        "To read your notes on a phone:\n"
        "1. Point your repository at a folder inside your Google Drive "
        "(for example Google Drive/YanaNotes).\n"
        "2. Let the desktop Google Drive client keep it synced.\n"
        "3. Open the Google Drive app on your phone to view the same notes.\n\n"
        "Native in app Drive sign in arrives once Google Cloud OAuth "
        "credentials are configured."
    )
