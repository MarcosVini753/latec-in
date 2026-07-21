from rest_framework import serializers

from apps.institutional.serializers import InstitutionalUnitSummarySerializer
from apps.metrics.models import ImpactMetric


class ImpactMetricSerializer(serializers.ModelSerializer):
    unit = InstitutionalUnitSummarySerializer(read_only=True)

    class Meta:
        model = ImpactMetric
        fields = ("unit", "key", "label", "value", "suffix", "description", "display_order")
