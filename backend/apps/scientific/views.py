from apps.common.viewsets import PublicReadOnlyModelViewSet
from apps.scientific.models import ScientificOutput
from apps.scientific.serializers import ScientificOutputSerializer


class ScientificOutputViewSet(PublicReadOnlyModelViewSet):
    queryset = ScientificOutput.objects.select_related("unit", "axis__unit").prefetch_related(
        "axis__mentorships__person__role"
    )
    serializer_class = ScientificOutputSerializer
    search_fields = ("title", "authors", "abstract")
