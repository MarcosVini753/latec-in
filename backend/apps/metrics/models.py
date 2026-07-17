from django.db import models

from apps.common.models import BaseModel


class ImpactMetric(BaseModel):
    unit = models.ForeignKey(
        "institutional.InstitutionalUnit",
        on_delete=models.SET_NULL,
        related_name="impact_metrics",
        blank=True,
        null=True,
    )
    key = models.SlugField(max_length=80, unique=True)
    label = models.CharField(max_length=120)
    value = models.PositiveIntegerField(default=0)
    suffix = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "label")
        verbose_name = "métrica de impacto"
        verbose_name_plural = "métricas de impacto"

    def __str__(self) -> str:
        return self.label


class MetricSnapshot(BaseModel):
    metric = models.ForeignKey(ImpactMetric, on_delete=models.CASCADE, related_name="snapshots")
    value = models.PositiveIntegerField(default=0)
    reference_date = models.DateField()
    note = models.TextField(blank=True)

    class Meta:
        ordering = ("-reference_date", "metric__label")
        constraints = [
            models.UniqueConstraint(fields=("metric", "reference_date"), name="unique_metric_snapshot_date"),
        ]
        verbose_name = "snapshot de métrica"
        verbose_name_plural = "snapshots de métricas"

    def __str__(self) -> str:
        return f"{self.metric}: {self.value} em {self.reference_date}"
