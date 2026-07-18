from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view

from apps.common.viewsets import PublicReadOnlyModelViewSet
from apps.scientific.models import ScientificOutput
from apps.scientific.serializers import ScientificOutputSerializer


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter("unit", OpenApiTypes.STR, description="Slug da unidade institucional."),
            OpenApiParameter("axis", OpenApiTypes.STR, description="Slug do eixo de pesquisa."),
            OpenApiParameter("year", OpenApiTypes.INT, description="Ano de publicação."),
            OpenApiParameter("featured", OpenApiTypes.BOOL, description="Filtra itens em destaque."),
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
        "axis__mentorships__person__role",
        "authorships__person__role",
    )
    serializer_class = ScientificOutputSerializer
    search_fields = ("title", "authors", "abstract")
