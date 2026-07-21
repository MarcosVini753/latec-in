from django.contrib import admin

from apps.common.admin_actions import EDITORIAL_ADMIN_ACTIONS
from apps.common.admin_scoping import UnitScopedAdminMixin, UnitScopedInlineMixin
from apps.scientific.models import ScientificAuthorship, ScientificOutput


class ScientificAuthorshipInline(UnitScopedInlineMixin, admin.TabularInline):
    model = ScientificAuthorship
    extra = 0
    autocomplete_fields = ("person",)


@admin.register(ScientificOutput)
class ScientificOutputAdmin(UnitScopedAdminMixin, admin.ModelAdmin):
    axis_lookup = "axis"
    list_display = ("title", "unit", "output_type", "axis", "editorial_status", "include_in_parent_ecosystem", "publication_date")
    list_filter = ("unit", "axis", "output_type", "editorial_status", "include_in_parent_ecosystem")
    search_fields = (
        "title",
        "abstract",
        "unit__name",
        "unit__acronym",
        "authorships__person__full_name",
    )
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("unit", "axis", "research_project", "academic_work")
    list_select_related = ("unit", "axis", "research_project", "academic_work")
    actions = EDITORIAL_ADMIN_ACTIONS
    fieldsets = (
        (
            "Identificação",
            {
                "fields": (
                    "unit",
                    "title",
                    "slug",
                    "output_type",
                    "axis",
                    "research_project",
                    "academic_work",
                )
            },
        ),
        ("Conteúdo", {"fields": ("abstract", "publication_date", "file", "external_url")}),
        ("Publicação", {"fields": ("editorial_status", "published_at", "include_in_parent_ecosystem")}),
    )
    inlines = (ScientificAuthorshipInline,)


@admin.register(ScientificAuthorship)
class ScientificAuthorshipAdmin(UnitScopedAdminMixin, admin.ModelAdmin):
    unit_lookup = "scientific_output__unit"
    axis_lookup = "scientific_output__axis"
    publication_lookup = "scientific_output"
    list_display = ("scientific_output", "person", "author_order", "author_role")
    list_filter = ("author_role",)
    search_fields = ("scientific_output__title", "person__full_name", "author_role")
    autocomplete_fields = ("scientific_output", "person")
