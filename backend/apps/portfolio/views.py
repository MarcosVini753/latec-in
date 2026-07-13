from apps.common.viewsets import PublicReadOnlyModelViewSet
from apps.portfolio.models import Project, ProjectCategory
from apps.portfolio.serializers import ProjectCategorySerializer, ProjectSerializer


class ProjectCategoryViewSet(PublicReadOnlyModelViewSet):
    queryset = ProjectCategory.objects.all()
    serializer_class = ProjectCategorySerializer
    search_fields = ("name", "description")


class ProjectViewSet(PublicReadOnlyModelViewSet):
    queryset = Project.objects.select_related("axis", "category", "status").prefetch_related(
        "team_members__person__role",
        "results",
        "links",
    )
    serializer_class = ProjectSerializer
    search_fields = ("title", "summary", "area", "problem", "solution")
