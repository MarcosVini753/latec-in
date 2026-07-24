from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view

from apps.common.viewsets import ECOSYSTEM_UNIT_PARAMETER, PublicReadOnlyModelViewSet
from apps.scientific.models import ScientificOutput
from apps.scientific.serializers import ScientificOutputSerializer


@extend_schema_view(
    list=extend_schema(
        parameters=[
            ECOSYSTEM_UNIT_PARAMETER,
            OpenApiParameter("axis", OpenApiTypes.STR, description="Slug do eixo de pesquisa."),
            OpenApiParameter("year", OpenApiTypes.INT, description="Ano de publicação."),
            OpenApiParameter("search", OpenApiTypes.STR, description="Busca textual."),
        ],
    ),
)
class ScientificOutputViewSet(PublicReadOnlyModelViewSet):
    queryset = ScientificOutput.objects.select_related(
        "unit",
        "axis__unit",
        "research_project",
        "academic_work",
    ).prefetch_related(
        "axis__mentorships__person",
        "authorships__person",
    )
    serializer_class = ScientificOutputSerializer
    search_fields = ("title", "abstract")
