from django.contrib import admin

from apps.common.admin_actions import EDITORIAL_ADMIN_ACTIONS
from apps.learning.models import Course, CourseMaterial, Event, LearningTrack


@admin.register(LearningTrack)
class LearningTrackAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "display_order")
    list_filter = ("is_active",)
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}


class CourseMaterialInline(admin.TabularInline):
    model = CourseMaterial
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "track", "axis", "enrollment_status", "editorial_status", "is_published", "is_featured", "start_date")
    list_filter = ("track", "axis", "enrollment_status", "editorial_status", "is_published", "is_featured")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("track", "axis", "instructors")
    actions = EDITORIAL_ADMIN_ACTIONS
    fieldsets = (
        ("Identificação", {"fields": ("title", "slug", "track", "axis", "instructors")}),
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
    list_display = ("title", "event_type", "axis", "event_status", "editorial_status", "is_published", "is_featured", "start_date")
    list_filter = ("event_type", "axis", "event_status", "editorial_status", "is_published", "is_featured")
    search_fields = ("title", "description", "location")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("axis",)
    actions = EDITORIAL_ADMIN_ACTIONS
    fieldsets = (
        ("Identificação", {"fields": ("title", "slug", "event_type", "axis")}),
        ("Conteúdo", {"fields": ("description",)}),
        ("Agenda e inscrição", {"fields": ("start_date", "end_date", "location", "event_status", "registration_url")}),
        ("Publicação", {"fields": ("editorial_status", "is_published", "published_at", "is_featured", "display_order")}),
    )
