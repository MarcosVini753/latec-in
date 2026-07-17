from django.contrib import admin

from apps.common.admin_actions import EDITORIAL_ADMIN_ACTIONS
from apps.transparency.models import TransparencyDocument


@admin.register(TransparencyDocument)
class TransparencyDocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "unit", "document_type", "status", "is_published", "is_featured", "publication_date")
    list_filter = ("unit", "document_type", "status", "is_published", "is_featured")
    search_fields = ("title", "description", "related_process", "unit__name", "unit__acronym")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("unit",)
    list_select_related = ("unit",)
    actions = EDITORIAL_ADMIN_ACTIONS
    fieldsets = (
        ("Identificação", {"fields": ("unit", "title", "slug", "document_type", "related_process")}),
        ("Conteúdo", {"fields": ("description", "file", "publication_date")}),
        ("Publicação", {"fields": ("status", "is_published", "published_at", "is_featured", "display_order")}),
    )
