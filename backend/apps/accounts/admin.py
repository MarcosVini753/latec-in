from django.contrib import admin

from apps.accounts.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "person", "role", "is_active_admin", "updated_at")
    list_filter = ("role", "is_active_admin")
    search_fields = ("user__username", "user__first_name", "user__last_name", "person__full_name")
    autocomplete_fields = ("user", "person")
