from django.contrib import admin

from apps.common.admin_actions import EDITORIAL_ADMIN_ACTIONS
from apps.common.admin_scoping import UnitScopedAdminMixin, UnitScopedInlineMixin
from apps.research.models import (
    AcademicWork,
    AcademicWorkContributor,
    ResearchProject,
    ResearchProjectMember,
)


class ResearchProjectMemberInline(UnitScopedInlineMixin, admin.TabularInline):
    model = ResearchProjectMember
    extra = 0
    autocomplete_fields = ("person",)


@admin.register(ResearchProject)
class ResearchProjectAdmin(UnitScopedAdminMixin, admin.ModelAdmin):
    axis_lookup = "axis"
    list_display = (
        "title",
        "unit",
        "axis",
        "project_status",
        "editorial_status",
        "include_in_parent_ecosystem",
        "start_date",
    )
    list_filter = (
        "unit",
        "axis",
        "project_status",
        "editorial_status",
        "include_in_parent_ecosystem",
    )
    search_fields = (
        "title",
        "summary",
        "unit__name",
        "unit__acronym",
    )
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("unit", "axis")
    list_select_related = ("unit", "axis")
    actions = EDITORIAL_ADMIN_ACTIONS
    fieldsets = (
        ("Identificação", {"fields": ("unit", "axis", "title", "slug", "project_status")}),
        ("Conteúdo", {"fields": ("summary", "file", "external_url")}),
        ("Período", {"fields": ("start_date", "end_date")}),
        (
            "Publicação",
            {
                "fields": (
                    "editorial_status",
                    "published_at",
                    "include_in_parent_ecosystem",
                )
            },
        ),
    )
    inlines = (ResearchProjectMemberInline,)


@admin.register(ResearchProjectMember)
class ResearchProjectMemberAdmin(UnitScopedAdminMixin, admin.ModelAdmin):
    unit_lookup = "research_project__unit"
    axis_lookup = "research_project__axis"
    publication_lookup = "research_project"
    list_display = ("research_project", "person", "role", "display_order")
    list_filter = ("role",)
    search_fields = ("research_project__title", "person__full_name")
    autocomplete_fields = ("research_project", "person")


class AcademicWorkContributorInline(UnitScopedInlineMixin, admin.TabularInline):
    model = AcademicWorkContributor
    extra = 0
    autocomplete_fields = ("person",)


@admin.register(AcademicWork)
class AcademicWorkAdmin(UnitScopedAdminMixin, admin.ModelAdmin):
    axis_lookup = "research_project__axis"
    list_display = (
        "title",
        "unit",
        "work_type",
        "research_project",
        "year",
        "editorial_status",
        "include_in_parent_ecosystem",
    )
    list_filter = ("unit", "work_type", "year", "editorial_status", "include_in_parent_ecosystem")
    search_fields = (
        "title",
        "course",
        "institution",
        "abstract",
        "keywords",
        "unit__name",
        "unit__acronym",
    )
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("unit", "research_project")
    list_select_related = ("unit", "research_project")
    actions = EDITORIAL_ADMIN_ACTIONS
    fieldsets = (
        ("Identificação", {"fields": ("unit", "research_project", "title", "slug", "work_type")}),
        ("Dados acadêmicos", {"fields": ("course", "institution", "year", "abstract", "keywords")}),
        ("Arquivo e acesso", {"fields": ("file", "external_url")}),
        (
            "Publicação",
            {
                "fields": (
                    "editorial_status",
                    "published_at",
                    "include_in_parent_ecosystem",
                )
            },
        ),
    )
    inlines = (AcademicWorkContributorInline,)


@admin.register(AcademicWorkContributor)
class AcademicWorkContributorAdmin(UnitScopedAdminMixin, admin.ModelAdmin):
    unit_lookup = "academic_work__unit"
    axis_lookup = "academic_work__research_project__axis"
    publication_lookup = "academic_work"
    list_display = ("academic_work", "person", "role", "display_order")
    list_filter = ("role",)
    search_fields = ("academic_work__title", "person__full_name")
    autocomplete_fields = ("academic_work", "person")
