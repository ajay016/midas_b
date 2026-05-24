"""
Playwright-based Midasbuy login.

Saves:
  session_dir/storage_state.json  - full browser state (cookies + localStorage)
  session_dir/cookies.json        - flat cookie list for easy httpx use
  session_dir/meta.json           - login metadata
"""
import json
import os
import time
import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class LoginResult:
    success: bool
    message: str
    session_dir: str = ""


def login_account_and_persist(account, base_dir: str) -> LoginResult:
    """
    Log in to Midasbuy with Playwright and save the session to disk.
    Returns a LoginResult.
    """
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    except ImportError:
        return LoginResult(False, "Playwright is not installed. Run: pip install playwright && playwright install chromium")

    session_dir = account.get_session_dir(base_dir)
    Path(session_dir).mkdir(parents=True, exist_ok=True)
    storage_state_path = os.path.join(session_dir, "storage_state.json")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
            )
            page = context.new_page()

            try:
                page.goto("https://www.midasbuy.com/midasbuy/login", timeout=60_000)
                page.wait_for_load_state("networkidle", timeout=30_000)
                time.sleep(2)

                # Try email + password login form
                email_sel    = 'input[type="email"], input[name="email"], input[placeholder*="email" i]'
                password_sel = 'input[type="password"]'

                page.wait_for_selector(email_sel, timeout=15_000)
                page.fill(email_sel, account.email)
                page.fill(password_sel, account.password)
                time.sleep(0.5)

                # Click login / submit
                page.keyboard.press("Enter")

                # Wait for redirect away from login page
                page.wait_for_url(lambda u: "login" not in u, timeout=30_000)
                time.sleep(3)

            except PWTimeout:
                # Already on a non-login page (maybe already logged in) — continue
                pass

            # Persist session
            state = context.storage_state()
            with open(storage_state_path, "w") as f:
                json.dump(state, f)

            # Also save a flat cookies.json (Playwright format → list of dicts)
            cookies_path = os.path.join(session_dir, "cookies.json")
            with open(cookies_path, "w") as f:
                json.dump(state.get("cookies", []), f, indent=2)

            # Meta
            meta_path = os.path.join(session_dir, "meta.json")
            with open(meta_path, "w") as f:
                json.dump({"email": account.email, "login_time": time.time()}, f)

            browser.close()

        # Check if session_token cookie is present (indicates login succeeded)
        with open(storage_state_path) as f:
            saved_state = json.load(f)

        has_session = any(
            c.get("name") in ("session_token", "SESSION", "auth_token")
            for c in saved_state.get("cookies", [])
        )

        if not has_session:
            return LoginResult(False, "Login may have failed — no session_token found. Check credentials.", session_dir)

        return LoginResult(True, "Logged in successfully", session_dir)

    except Exception as exc:
        logger.exception("Playwright login failed for %s", account.email)
        return LoginResult(False, str(exc), session_dir)
