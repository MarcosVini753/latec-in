from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view

from apps.common.viewsets import ECOSYSTEM_UNIT_PARAMETER, PublicReadOnlyModelViewSet
from apps.research.models import AcademicWork, ResearchProject
from apps.research.serializers import AcademicWorkSerializer, ResearchProjectSerializer


COMMON_FILTERS = [
    ECOSYSTEM_UNIT_PARAMETER,
    OpenApiParameter("year", OpenApiTypes.INT, description="Ano do conteúdo."),
    OpenApiParameter("search", OpenApiTypes.STR, description="Busca textual."),
]


@extend_schema_view(
    list=extend_schema(
        parameters=COMMON_FILTERS
        + [
            OpenApiParameter("axis", OpenApiTypes.STR, description="Slug do eixo de pesquisa."),
            OpenApiParameter(
                "project_status",
                OpenApiTypes.STR,
                enum=ResearchProject.ProjectStatus.values,
                description="Status de execução da pesquisa.",
            ),
        ],
    ),
)
class ResearchProjectViewSet(PublicReadOnlyModelViewSet):
    queryset = ResearchProject.objects.select_related("unit", "axis__unit").prefetch_related(
        "axis__mentorships__person",
        "team_members__person",
    )
    serializer_class = ResearchProjectSerializer
    search_fields = ("title", "summary")

    def get_queryset(self):
        queryset = super().get_queryset()
        project_status = self.request.query_params.get("project_status")
        return queryset.filter(project_status=project_status) if project_status else queryset


@extend_schema_view(
    list=extend_schema(
        parameters=COMMON_FILTERS
        + [
            OpenApiParameter(
                "work_type",
                OpenApiTypes.STR,
                enum=AcademicWork.WorkType.values,
                description="Tipo de trabalho acadêmico.",
            ),
        ],
    ),
)
class AcademicWorkViewSet(PublicReadOnlyModelViewSet):
    queryset = AcademicWork.objects.select_related("unit", "research_project").prefetch_related(
        "work_contributors__person",
    )
    serializer_class = AcademicWorkSerializer
    search_fields = ("title", "course", "institution", "abstract", "keywords")

    def get_queryset(self):
        queryset = super().get_queryset()
        work_type = self.request.query_params.get("work_type")
        return queryset.filter(work_type=work_type) if work_type else queryset
