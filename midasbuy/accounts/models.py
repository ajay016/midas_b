from django.db import models


class MidasbuyAccount(models.Model):
    STATUS_CHOICES = [
        (0, "Logged Out"),
        (1, "Logged In"),
        (2, "Login Failed"),
        (3, "Session Expired"),
    ]

    label        = models.CharField(max_length=100, help_text="Friendly name for this account")
    email        = models.EmailField(unique=True)
    password     = models.CharField(max_length=255)
    phone        = models.CharField(max_length=20, blank=True, null=True)

    status       = models.IntegerField(choices=STATUS_CHOICES, default=0)
    session_dir  = models.CharField(max_length=500, blank=True, null=True,
                                    help_text="Path to folder with storage_state.json + cookies.json")
    last_error   = models.TextField(blank=True, null=True)
    last_login   = models.DateTimeField(blank=True, null=True)

    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.label or self.email

    def get_session_dir(self, base_dir):
        import os
        return os.path.join(base_dir, "midasbuy_sessions", f"account_{self.pk}")

    def has_valid_session(self):
        import os
        if not self.session_dir:
            return False
        return os.path.exists(os.path.join(self.session_dir, "storage_state.json"))

    def get_cookie_header(self):
        """Return cookies as a header string for httpx/requests."""
        import json, os
        cookie_path = os.path.join(self.session_dir or "", "cookies.json")
        if not os.path.exists(cookie_path):
            return ""
        with open(cookie_path) as f:
            cookies = json.load(f)
        return "; ".join(f"{c['name']}={c['value']}" for c in cookies)
