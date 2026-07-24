from django.contrib import admin

from apps.common.admin_scoping import UnitScopedAdminMixin, UnitScopedInlineMixin
from apps.metrics.models import ImpactMetric, MetricSnapshot


class MetricSnapshotInline(UnitScopedInlineMixin, admin.TabularInline):
    model = MetricSnapshot
    extra = 0


@admin.register(ImpactMetric)
class ImpactMetricAdmin(UnitScopedAdminMixin, admin.ModelAdmin):
    list_display = ("label", "unit", "key", "value", "suffix", "is_active", "display_order")
    list_filter = ("unit", "is_active")
    search_fields = ("label", "key", "description", "unit__name", "unit__acronym")
    prepopulated_fields = {"key": ("label",)}
    autocomplete_fields = ("unit",)
    list_select_related = ("unit",)
    fieldsets = (
        ("Identificação", {"fields": ("unit", "label", "key")}),
        ("Valor", {"fields": ("value", "suffix", "description")}),
        ("Exibição", {"fields": ("is_active", "display_order")}),
    )
    inlines = (MetricSnapshotInline,)


@admin.register(MetricSnapshot)
class MetricSnapshotAdmin(UnitScopedAdminMixin, admin.ModelAdmin):
    unit_lookup = "metric__unit"
    publication_lookup = "metric"
    list_display = ("metric", "value", "reference_date")
    list_filter = ("metric", "reference_date")
    search_fields = ("metric__label", "note")
    autocomplete_fields = ("metric",)
