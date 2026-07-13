from django.contrib import admin

from apps.axes.models import AxisMentorship, ResearchAxis


class AxisMentorshipInline(admin.TabularInline):
    model = AxisMentorship
    extra = 0
    autocomplete_fields = ("person",)


@admin.register(ResearchAxis)
class ResearchAxisAdmin(admin.ModelAdmin):
    list_display = ("number", "title", "is_active", "display_order")
    list_filter = ("is_active",)
    search_fields = ("title", "description", "keywords")
    prepopulated_fields = {"slug": ("title",)}
    inlines = (AxisMentorshipInline,)


@admin.register(AxisMentorship)
class AxisMentorshipAdmin(admin.ModelAdmin):
    list_display = ("axis", "person", "role", "is_main_mentor", "display_order")
    list_filter = ("axis", "role", "is_main_mentor")
    search_fields = ("axis__title", "person__full_name", "role")
    autocomplete_fields = ("axis", "person")
