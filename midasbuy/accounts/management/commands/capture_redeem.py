"""
Debug capture for the redeem COMMIT step.

Opens a HEADFUL Midasbuy redeem page using a logged-in account's session, with
full network capture (every request + response body for non-asset traffic), and
keeps the browser open so you can perform the real redemption by hand while we
record exactly which request commits the code.

Usage:
    python manage.py capture_redeem --account-id 1 --country bd --minutes 30

Then in the opened browser: look up the player, enter the VALID code, click OK,
solve the captcha if prompted, and confirm the final popup. Everything is written
to  midasbuy_sessions/account_<id>/redeem_commit_capture.txt  — send that file.

NOTE: a valid code is consumed by a real redemption. This captures HOW it happens
so the commit can be automated afterwards.
"""
import json
import os
import time

from django.conf import settings
from django.core.management.base import BaseCommand


# Requests whose bodies we always capture in full (the interesting ones).
_FULL_BODY_HINTS = (
    "/interface/", "shelfproto", "redeem", "order", "secondary", "buy",
    "shelves_svr", "harvestsharp", "commoncheck", "pavalidate", "trade",
    "provide", "confirm", "/pay", "deliver", "commit",
)
# Resource types whose bodies we skip (too big / not useful).
_SKIP_BODY_TYPES = {"image", "font", "media", "stylesheet"}


class Command(BaseCommand):
    help = "Open a headful Midasbuy redeem page with full network capture to debug the redemption commit."

    def add_arguments(self, parser):
        parser.add_argument("--account-id", type=int, default=1)
        parser.add_argument("--country", default="bd")
        parser.add_argument("--minutes", type=int, default=30)

    def handle(self, *args, **opts):
        from accounts.models import MidasbuyAccount
        from accounts.services.playwright_crypto import (
            _get_playwright,
            _launch_context,
            _setup_chaos_vm_protection,
            _wait_for_xmidas,
        )

        acct = MidasbuyAccount.objects.get(pk=opts["account_id"])
        ssp = acct.storage_state_path or os.path.join(
            acct.get_session_dir(str(settings.BASE_DIR)), "storage_state.json"
        )
        if not ssp or not os.path.exists(ssp):
            self.stderr.write(f"storage_state not found for account {opts['account_id']}: {ssp}")
            return

        country = opts["country"]
        out_dir = os.path.dirname(ssp)
        cap_path = os.path.join(out_dir, "redeem_commit_capture.txt")
        # Same URL the working crypto flow uses, so window.xMidas initialises.
        redeem_url = f"https://www.midasbuy.com/midasbuy/{country}/redeem/pubgm?from=self.midasbuy_saas"

        with open(cap_path, "w", encoding="utf-8") as f:
            f.write(f"# redeem commit capture  account={opts['account_id']}  {time.ctime()}\n")

        def dump(line: str):
            try:
                with open(cap_path, "a", encoding="utf-8") as f:
                    f.write(line + "\n")
            except Exception:
                pass

        sync_playwright, _ = _get_playwright()

        self.stdout.write(self.style.WARNING(
            "Opening headful browser. Do the FULL redemption by hand (look up player, "
            "enter the VALID code, OK, solve captcha, confirm). Capturing to:\n  " + cap_path
        ))

        with sync_playwright() as p:
            # Reuse the working flow's launch (stealth + storage_state + SERVER_DATA
            # snapshot) but headful, so the real page's player lookup / encryption works.
            browser, context = _launch_context(p, ssp, country, headless=False)
            page = context.new_page()
            _setup_chaos_vm_protection(page)

            def on_request(req):
                try:
                    u = req.url
                    interesting = any(h in u.lower() for h in _FULL_BODY_HINTS)
                    if interesting or req.method != "GET":
                        dump(f"\n>> {req.method} {u}")
                        pd = None
                        try:
                            pd = req.post_data
                        except Exception:
                            pd = None
                        if pd:
                            dump("POST_DATA: " + pd[:20000])
                except Exception:
                    pass

            def on_response(resp):
                try:
                    u = resp.url
                    rtype = resp.request.resource_type
                    interesting = any(h in u.lower() for h in _FULL_BODY_HINTS)
                    if interesting:
                        dump(f"\n<< {resp.status} {u}")
                        if rtype not in _SKIP_BODY_TYPES:
                            body = None
                            try:
                                body = resp.text()
                            except Exception:
                                body = None
                            if body:
                                dump(body[:40000])
                        self.stdout.write(f"  captured {resp.status} {u[:110]}")
                except Exception:
                    pass

            page.on("request", on_request)
            page.on("response", on_response)

            page.goto(redeem_url, wait_until="load")
            try:
                _wait_for_xmidas(page, out_dir, 30_000)
            except Exception:
                pass
            self.stdout.write(self.style.SUCCESS(
                f"Browser open at {redeem_url}. Complete the redemption now."
            ))

            deadline = time.time() + opts["minutes"] * 60
            sentinel = os.path.join(out_dir, "stop_capture.txt")
            self.stdout.write(f"Capturing for up to {opts['minutes']} min. "
                              f"Create {sentinel} (or close the window) to stop early.")
            try:
                while time.time() < deadline:
                    if page.is_closed() or os.path.exists(sentinel):
                        break
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
            finally:
                if os.path.exists(sentinel):
                    try:
                        os.remove(sentinel)
                    except Exception:
                        pass
                try:
                    context.close()
                except Exception:
                    pass
                try:
                    browser.close()
                except Exception:
                    pass

        self.stdout.write(self.style.SUCCESS(f"Done. Capture saved to: {cap_path}"))
