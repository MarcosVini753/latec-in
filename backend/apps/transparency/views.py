from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view

from apps.common.viewsets import ECOSYSTEM_UNIT_PARAMETER, PublicReadOnlyModelViewSet
from apps.transparency.models import TransparencyDocument
from apps.transparency.serializers import TransparencyDocumentSerializer


@extend_schema_view(
    list=extend_schema(
        parameters=[
            ECOSYSTEM_UNIT_PARAMETER,
            OpenApiParameter("year", OpenApiTypes.INT, description="Ano de publicação."),
            OpenApiParameter("search", OpenApiTypes.STR, description="Busca textual."),
        ],
    ),
)
class TransparencyDocumentViewSet(PublicReadOnlyModelViewSet):
    queryset = TransparencyDocument.objects.select_related("unit")
    serializer_class = TransparencyDocumentSerializer
    search_fields = ("title", "description", "related_process")
