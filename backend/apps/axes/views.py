from apps.axes.models import ResearchAxis
from apps.axes.serializers import ResearchAxisSerializer
from apps.common.viewsets import PublicReadOnlyModelViewSet


class ResearchAxisViewSet(PublicReadOnlyModelViewSet):
    queryset = ResearchAxis.objects.select_related("unit").prefetch_related("mentorships__person")
    serializer_class = ResearchAxisSerializer
    search_fields = ("title", "description", "keywords")
