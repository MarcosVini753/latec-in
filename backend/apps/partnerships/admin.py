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
    list_display = ("subject", "contact_type", "name", "email", "organization", "status", "created_at", "responded_at")
    list_filter = ("contact_type", "status", "created_at", "responded_at")
    search_fields = ("subject", "name", "email", "organization", "message")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Mensagem", {"fields": ("contact_type", "subject", "message", "status")}),
        ("Contato", {"fields": ("name", "email", "organization")}),
        ("Atendimento", {"fields": ("responded_at",)}),
        ("Auditoria", {"fields": ("created_at", "updated_at")}),
    )
