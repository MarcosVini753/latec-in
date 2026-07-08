from django.contrib import admin

from apps.metrics.models import ImpactMetric, MetricSnapshot


class MetricSnapshotInline(admin.TabularInline):
    model = MetricSnapshot
    extra = 0


@admin.register(ImpactMetric)
class ImpactMetricAdmin(admin.ModelAdmin):
    list_display = ("label", "key", "value", "suffix", "is_active", "display_order")
    list_filter = ("is_active",)
    search_fields = ("label", "key", "description")
    prepopulated_fields = {"key": ("label",)}
    inlines = (MetricSnapshotInline,)


@admin.register(MetricSnapshot)
class MetricSnapshotAdmin(admin.ModelAdmin):
    list_display = ("metric", "value", "reference_date")
    list_filter = ("metric", "reference_date")
    search_fields = ("metric__label", "note")
    autocomplete_fields = ("metric",)
