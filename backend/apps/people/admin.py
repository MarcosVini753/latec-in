from django.contrib import admin

from apps.common.admin_scoping import ReferenceAdminMixin
from apps.people.models import Person, Role


@admin.register(Role)
class RoleAdmin(ReferenceAdminMixin, admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "display_order")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Person)
class PersonAdmin(ReferenceAdminMixin, admin.ModelAdmin):
    unit_lookup = "institution_memberships__unit"
    unit_lookup_is_many = True
    mentor_requires_axis = False
    management_access = "scoped"
    list_display = ("full_name", "role", "is_active", "is_featured", "display_order")
    list_filter = ("role", "is_active", "is_featured")
    search_fields = ("full_name", "short_bio", "email")
    prepopulated_fields = {"slug": ("full_name",)}
    autocomplete_fields = ("role",)
