from django.contrib import admin

from .models import MidasbuyAccount, MidasbuyLoginAttempt


@admin.register(MidasbuyAccount)
class MidasbuyAccountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "label",
        "email",
        "status",
        "last_login_at",
        "updated_at",
    )
    list_filter = ("status", "created_at", "updated_at")
    search_fields = ("label", "email", "phone")
    readonly_fields = ("created_at", "updated_at", "last_login", "last_login_at")
    exclude = (
        "password",
        "cookie_data",
        "storage_state_data",
        "session_path",
        "storage_state_path",
        "token_path",
    )


@admin.register(MidasbuyLoginAttempt)
class MidasbuyLoginAttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "account", "result", "created_at")
    list_filter = ("result", "created_at")
    search_fields = ("account__label", "account__email", "message")
    readonly_fields = (
        "account",
        "result",
        "message",
        "screenshot_path",
        "html_snapshot_path",
        "created_at",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
