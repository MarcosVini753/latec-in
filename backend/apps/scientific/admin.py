from django.contrib import admin

from apps.common.admin_actions import EDITORIAL_ADMIN_ACTIONS
from apps.scientific.models import ScientificOutput


@admin.register(ScientificOutput)
class ScientificOutputAdmin(admin.ModelAdmin):
    list_display = ("title", "unit", "output_type", "axis", "status", "is_published", "is_featured", "publication_date")
    list_filter = ("unit", "axis", "output_type", "status", "is_published", "is_featured")
    search_fields = ("title", "authors", "abstract", "unit__name", "unit__acronym")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("unit", "axis")
    list_select_related = ("unit", "axis")
    actions = EDITORIAL_ADMIN_ACTIONS
    fieldsets = (
        ("Identificação", {"fields": ("unit", "title", "slug", "output_type", "axis", "authors")}),
        ("Conteúdo", {"fields": ("abstract", "publication_date", "file", "external_url")}),
        ("Publicação", {"fields": ("status", "is_published", "published_at", "is_featured", "display_order")}),
    )
