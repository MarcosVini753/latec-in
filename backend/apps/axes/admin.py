from django.contrib import admin

from apps.axes.models import AxisMentorship, ResearchAxis
from apps.common.admin_scoping import UnitScopedAdminMixin, UnitScopedInlineMixin


class AxisMentorshipInline(UnitScopedInlineMixin, admin.TabularInline):
    model = AxisMentorship
    extra = 0
    autocomplete_fields = ("person",)


@admin.register(ResearchAxis)
class ResearchAxisAdmin(UnitScopedAdminMixin, admin.ModelAdmin):
    axis_lookup = "pk"
    list_display = ("number", "title", "unit", "is_active", "display_order")
    list_filter = ("unit", "is_active")
    search_fields = ("title", "description", "keywords", "unit__name", "unit__acronym")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("unit",)
    list_select_related = ("unit",)
    fieldsets = (
        ("Identificação", {"fields": ("unit", "number", "title", "slug")}),
        ("Conteúdo", {"fields": ("description", "keywords")}),
        ("Exibição", {"fields": ("is_active", "display_order")}),
    )
    inlines = (AxisMentorshipInline,)


@admin.register(AxisMentorship)
class AxisMentorshipAdmin(UnitScopedAdminMixin, admin.ModelAdmin):
    unit_lookup = "axis__unit"
    axis_lookup = "axis"
    publication_lookup = "axis"
    list_display = ("axis", "person", "role", "is_main_mentor", "display_order")
    list_filter = ("axis", "role", "is_main_mentor")
    search_fields = ("axis__title", "person__full_name", "role")
    autocomplete_fields = ("axis", "person")
