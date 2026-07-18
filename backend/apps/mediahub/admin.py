from django.contrib import admin

from apps.common.admin_scoping import UnitScopedAdminMixin
from apps.mediahub.models import MediaAsset


@admin.register(MediaAsset)
class MediaAssetAdmin(UnitScopedAdminMixin, admin.ModelAdmin):
    list_display = ("title", "unit", "asset_type", "is_public", "uploaded_by", "updated_at")
    list_filter = ("unit", "asset_type", "is_public")
    search_fields = ("title", "description", "alt_text", "credit", "unit__name", "unit__acronym")
    autocomplete_fields = ("unit", "uploaded_by")
    list_select_related = ("unit", "uploaded_by")
    fieldsets = (
        ("Identificação", {"fields": ("unit", "title", "asset_type")}),
        ("Arquivo", {"fields": ("file", "description", "alt_text", "credit")}),
        ("Controle", {"fields": ("is_public", "uploaded_by")}),
    )
