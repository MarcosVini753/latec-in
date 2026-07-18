from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User

from apps.accounts.models import Profile
from apps.common.admin_scoping import AdminOnlyAdminMixin


@admin.register(Profile)
class ProfileAdmin(AdminOnlyAdminMixin, admin.ModelAdmin):
    list_display = ("user", "person", "role", "primary_unit", "inherit_descendants", "is_active_admin", "updated_at")
    list_filter = ("role", "primary_unit", "inherit_descendants", "is_active_admin")
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "person__full_name",
        "primary_unit__name",
        "primary_unit__acronym",
    )
    autocomplete_fields = ("user", "person", "primary_unit", "authorized_units")


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class ScopedUserAdmin(AdminOnlyAdminMixin, UserAdmin):
    pass


@admin.register(Group)
class ScopedGroupAdmin(AdminOnlyAdminMixin, GroupAdmin):
    pass
