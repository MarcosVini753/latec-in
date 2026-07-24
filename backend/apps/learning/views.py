from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view

from apps.common.viewsets import ECOSYSTEM_UNIT_PARAMETER, PublicReadOnlyModelViewSet
from apps.learning.models import Course
from apps.learning.serializers import CourseSerializer


@extend_schema_view(
    list=extend_schema(
        parameters=[
            ECOSYSTEM_UNIT_PARAMETER,
            OpenApiParameter("axis", OpenApiTypes.STR, description="Slug do eixo de pesquisa."),
            OpenApiParameter("year", OpenApiTypes.INT, description="Ano de início."),
            OpenApiParameter("search", OpenApiTypes.STR, description="Busca textual."),
        ],
    ),
)
class CourseViewSet(PublicReadOnlyModelViewSet):
    queryset = Course.objects.select_related("unit", "axis__unit").prefetch_related(
        "axis__mentorships__person",
        "instructors",
        "materials",
    )
    serializer_class = CourseSerializer
    search_fields = ("title", "description")
