from django.contrib import admin

from apps.common.admin_actions import EDITORIAL_ADMIN_ACTIONS
from apps.core.models import HeroBanner, InstitutionalSection, SiteSettings, SocialLink


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "unit", "institution", "contact_email", "is_active", "updated_at")
    list_filter = ("unit", "is_active")
    search_fields = ("site_name", "institution", "description")
    autocomplete_fields = ("unit",)


@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ("title", "unit", "is_published", "display_order", "updated_at")
    list_filter = ("unit", "is_published")
    search_fields = ("title", "subtitle")
    autocomplete_fields = ("unit",)
    actions = EDITORIAL_ADMIN_ACTIONS
    fieldsets = (
        ("Conteúdo", {"fields": ("unit", "title", "subtitle", "image")}),
        ("Chamada para ação", {"fields": ("cta_label", "cta_url")}),
        ("Publicação", {"fields": ("is_published", "display_order")}),
    )


@admin.register(InstitutionalSection)
class InstitutionalSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "unit", "section_type", "is_published", "display_order")
    list_filter = ("unit", "section_type", "is_published")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("unit",)
    actions = EDITORIAL_ADMIN_ACTIONS
    fieldsets = (
        ("Identificação", {"fields": ("unit", "section_type", "title", "slug")}),
        ("Conteúdo", {"fields": ("content", "image")}),
        ("Publicação", {"fields": ("is_published", "display_order")}),
    )


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("label", "unit", "url", "is_active", "display_order")
    list_filter = ("unit", "is_active")
    search_fields = ("label", "url")
    autocomplete_fields = ("unit",)
