from django.contrib import admin
from django.core.exceptions import PermissionDenied

from apps.common.admin_scoping import (
    LabCoordinatorOnlyAdminMixin,
    UnitScopedAdminMixin,
    can_publish,
    get_admin_profile,
    is_global_admin,
)
from apps.partnerships.models import ContactMessage, Partner


@admin.register(Partner)
class PartnerAdmin(UnitScopedAdminMixin, admin.ModelAdmin):
    unit_lookup = "units"
    unit_lookup_is_many = True
    shared_units_lookup = "units"
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

    def _submitted_scope_is_allowed(self, request, obj):
        if is_global_admin(request):
            return True
        if obj.pk:
            return self.scope_queryset(request, obj.__class__._default_manager.filter(pk=obj.pk)).exists()
        profile = get_admin_profile(request)
        return bool(profile and profile.accessible_unit_ids())

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        unit_ids = set(form.instance.units.values_list("pk", flat=True))
        profile = get_admin_profile(request)
        if not is_global_admin(request) and (
            not profile
            or (not unit_ids and not profile.is_lab_coordinator)
            or not unit_ids.issubset(profile.accessible_unit_ids())
            or (len(unit_ids) > 1 and not can_publish(request))
        ):
            raise PermissionDenied("O parceiro compartilhado está fora do escopo institucional autorizado.")

    @admin.display(description="Unidades")
    def unit_list(self, obj):
        return ", ".join(unit.acronym or unit.name for unit in obj.units.all()) or "—"


@admin.register(ContactMessage)
class ContactMessageAdmin(LabCoordinatorOnlyAdminMixin, admin.ModelAdmin):
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
