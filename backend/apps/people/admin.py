from django.contrib import admin

from apps.common.admin_scoping import ReferenceAdminMixin
from apps.people.models import Person


@admin.register(Person)
class PersonAdmin(ReferenceAdminMixin, admin.ModelAdmin):
    unit_lookup = "institution_memberships__unit"
    unit_lookup_is_many = True
    mentor_requires_axis = False
    management_access = "scoped"
    list_display = ("full_name", "is_active", "display_order")
    list_filter = ("is_active",)
    search_fields = ("full_name", "short_bio", "email")
    prepopulated_fields = {"slug": ("full_name",)}
