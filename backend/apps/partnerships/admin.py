from django.contrib import admin

from apps.partnerships.models import ContactMessage, Partner


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "unit_list", "partner_type", "is_active", "display_order")
    list_filter = ("units", "partner_type", "is_active")
    search_fields = ("name", "description", "website", "units__name", "units__acronym")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("units",)
    fieldsets = (
        ("Identificação", {"fields": ("units", "name", "slug", "partner_type")}),
        ("Conteúdo", {"fields": ("description", "logo", "website")}),
        ("Exibição", {"fields": ("is_active", "display_order")}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("units")

    @admin.display(description="Unidades")
    def unit_list(self, obj):
        return ", ".join(unit.acronym or unit.name for unit in obj.units.all()) or "—"


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
