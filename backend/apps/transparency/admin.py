from django.contrib import admin

from apps.transparency.models import TransparencyDocument


@admin.register(TransparencyDocument)
class TransparencyDocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "document_type", "status", "is_published", "is_featured", "publication_date")
    list_filter = ("document_type", "status", "is_published", "is_featured")
    search_fields = ("title", "description", "related_process")
    prepopulated_fields = {"slug": ("title",)}
