from django.contrib import admin

from apps.partnerships.models import ContactMessage, Partner


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "partner_type", "is_active", "display_order")
    list_filter = ("partner_type", "is_active")
    search_fields = ("name", "description", "website")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "name", "email", "organization", "status", "created_at", "responded_at")
    list_filter = ("status", "created_at", "responded_at")
    search_fields = ("subject", "name", "email", "organization", "message")
    readonly_fields = ("created_at", "updated_at")
