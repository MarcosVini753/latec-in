from apps.common.viewsets import PublicReadOnlyModelViewSet
from apps.metrics.models import ImpactMetric
from apps.metrics.serializers import ImpactMetricSerializer


class ImpactMetricViewSet(PublicReadOnlyModelViewSet):
    lookup_field = "key"
    queryset = ImpactMetric.objects.select_related("unit")
    serializer_class = ImpactMetricSerializer
    search_fields = ("label", "description")
