from django.contrib import admin

from apps.core.models import HeroBanner, InstitutionalSection, SiteSettings, SocialLink


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "institution", "contact_email", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("site_name", "institution", "description")


@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "display_order", "updated_at")
    list_filter = ("is_published",)
    search_fields = ("title", "subtitle")


@admin.register(InstitutionalSection)
class InstitutionalSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "section_type", "is_published", "display_order")
    list_filter = ("section_type", "is_published")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("label", "url", "is_active", "display_order")
    list_filter = ("is_active",)
    search_fields = ("label", "url")
