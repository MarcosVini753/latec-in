from django.contrib import admin

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
    list_display = ("title", "track", "axis", "status", "is_published", "is_featured", "start_date")
    list_filter = ("track", "axis", "status", "is_published", "is_featured")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("track", "axis", "instructors")
    inlines = (CourseMaterialInline,)


@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "is_public", "display_order")
    list_filter = ("is_public",)
    search_fields = ("title", "description", "course__title")
    autocomplete_fields = ("course",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "event_type", "axis", "status", "is_published", "is_featured", "start_date")
    list_filter = ("event_type", "axis", "status", "is_published", "is_featured")
    search_fields = ("title", "description", "location")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("axis",)
