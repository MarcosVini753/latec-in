from django.contrib import admin

from apps.mediahub.models import MediaAsset


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ("title", "asset_type", "is_public", "uploaded_by", "updated_at")
    list_filter = ("asset_type", "is_public")
    search_fields = ("title", "description", "alt_text", "credit")
    autocomplete_fields = ("uploaded_by",)
