from django.contrib import admin

from apps.common.admin_actions import EDITORIAL_ADMIN_ACTIONS
from apps.common.admin_scoping import UnitScopedAdminMixin, UnitScopedInlineMixin
from apps.learning.models import Course, CourseMaterial


class CourseMaterialInline(UnitScopedInlineMixin, admin.TabularInline):
    model = CourseMaterial
    extra = 0


@admin.register(Course)
class CourseAdmin(UnitScopedAdminMixin, admin.ModelAdmin):
    axis_lookup = "axis"
    list_display = ("title", "unit", "axis", "enrollment_status", "editorial_status", "include_in_parent_ecosystem", "start_date")
    list_filter = ("unit", "axis", "enrollment_status", "editorial_status", "include_in_parent_ecosystem")
    search_fields = ("title", "description", "unit__name", "unit__acronym")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("unit", "axis", "instructors")
    list_select_related = ("unit", "axis")
    actions = EDITORIAL_ADMIN_ACTIONS
    fieldsets = (
        ("Identificação", {"fields": ("unit", "title", "slug", "axis", "instructors")}),
        ("Conteúdo", {"fields": ("description", "cover_image")}),
        ("Agenda e inscrição", {"fields": ("start_date", "end_date", "workload_hours", "enrollment_status", "registration_url")}),
        ("Publicação", {"fields": ("editorial_status", "published_at", "include_in_parent_ecosystem")}),
    )
    inlines = (CourseMaterialInline,)


@admin.register(CourseMaterial)
class CourseMaterialAdmin(UnitScopedAdminMixin, admin.ModelAdmin):
    unit_lookup = "course__unit"
    axis_lookup = "course__axis"
    publication_lookup = "course"
    list_display = ("title", "course", "display_order")
    search_fields = ("title", "description", "course__title")
    autocomplete_fields = ("course",)
