from django.contrib import admin

from apps.scientific.models import ScientificOutput


@admin.register(ScientificOutput)
class ScientificOutputAdmin(admin.ModelAdmin):
    list_display = ("title", "output_type", "axis", "status", "is_published", "is_featured", "publication_date")
    list_filter = ("axis", "output_type", "status", "is_published", "is_featured")
    search_fields = ("title", "authors", "abstract")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("axis",)
