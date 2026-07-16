from django.contrib import admin

from apps.institutional.models import InstitutionMembership, InstitutionalUnit


@admin.register(InstitutionalUnit)
class InstitutionalUnitAdmin(admin.ModelAdmin):
    list_display = ("hierarchy", "unit_type", "is_active", "is_public", "display_order")
    list_filter = ("unit_type", "is_active", "is_public", "parent")
    search_fields = ("name", "acronym", "description", "mission", "vision")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("parent",)
    list_select_related = ("parent",)

    @admin.display(description="Hierarquia", ordering="parent__name")
    def hierarchy(self, obj):
        return f"{obj.parent} › {obj}" if obj.parent else str(obj)


@admin.register(InstitutionMembership)
class InstitutionMembershipAdmin(admin.ModelAdmin):
    list_display = (
        "person",
        "unit",
        "role",
        "start_date",
        "end_date",
        "is_active",
        "is_public",
        "display_order",
    )
    list_filter = ("unit", "role", "is_active", "is_public")
    search_fields = ("person__full_name", "unit__name", "unit__acronym", "role")
    autocomplete_fields = ("person", "unit")
    list_select_related = ("person", "unit")
