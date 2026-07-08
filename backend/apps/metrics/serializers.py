from rest_framework import serializers

from apps.metrics.models import ImpactMetric


class ImpactMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpactMetric
        fields = ("key", "label", "value", "suffix", "description", "display_order")
