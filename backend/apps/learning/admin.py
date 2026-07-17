from django.contrib import admin

from apps.common.admin_actions import EDITORIAL_ADMIN_ACTIONS
from apps.learning.models import Course, CourseMaterial, Event, LearningTrack


@admin.register(LearningTrack)
class LearningTrackAdmin(admin.ModelAdmin):
    list_display = ("title", "unit", "is_active", "display_order")
    list_filter = ("unit", "is_active")
    search_fields = ("title", "description", "unit__name", "unit__acronym")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("unit",)
    list_select_related = ("unit",)
    fieldsets = (
        ("Identificação", {"fields": ("unit", "title", "slug")}),
        ("Conteúdo", {"fields": ("description",)}),
        ("Exibição", {"fields": ("is_active", "display_order")}),
    )


class CourseMaterialInline(admin.TabularInline):
    model = CourseMaterial
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "unit", "track", "axis", "enrollment_status", "editorial_status", "is_published", "is_featured", "start_date")
    list_filter = ("unit", "track", "axis", "enrollment_status", "editorial_status", "is_published", "is_featured")
    search_fields = ("title", "description", "unit__name", "unit__acronym")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("unit", "track", "axis", "instructors")
    list_select_related = ("unit", "track", "axis")
    actions = EDITORIAL_ADMIN_ACTIONS
    fieldsets = (
        ("Identificação", {"fields": ("unit", "title", "slug", "track", "axis", "instructors")}),
        ("Conteúdo", {"fields": ("description", "cover_image")}),
        ("Agenda e inscrição", {"fields": ("start_date", "end_date", "workload_hours", "enrollment_status", "registration_url")}),
        ("Publicação", {"fields": ("editorial_status", "is_published", "published_at", "is_featured", "display_order")}),
    )
    inlines = (CourseMaterialInline,)


@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "is_public", "display_order")
    list_filter = ("is_public",)
    search_fields = ("title", "description", "course__title")
    autocomplete_fields = ("course",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "unit", "event_type", "axis", "event_status", "editorial_status", "is_published", "is_featured", "start_date")
    list_filter = ("unit", "event_type", "axis", "event_status", "editorial_status", "is_published", "is_featured")
    search_fields = ("title", "description", "location", "unit__name", "unit__acronym")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("unit", "axis")
    list_select_related = ("unit", "axis")
    actions = EDITORIAL_ADMIN_ACTIONS
    fieldsets = (
        ("Identificação", {"fields": ("unit", "title", "slug", "event_type", "axis")}),
        ("Conteúdo", {"fields": ("description",)}),
        ("Agenda e inscrição", {"fields": ("start_date", "end_date", "location", "event_status", "registration_url")}),
        ("Publicação", {"fields": ("editorial_status", "is_published", "published_at", "is_featured", "display_order")}),
    )
