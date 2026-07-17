from apps.common.viewsets import PublicReadOnlyModelViewSet
from apps.transparency.models import TransparencyDocument
from apps.transparency.serializers import TransparencyDocumentSerializer


class TransparencyDocumentViewSet(PublicReadOnlyModelViewSet):
    queryset = TransparencyDocument.objects.select_related("unit")
    serializer_class = TransparencyDocumentSerializer
    search_fields = ("title", "description", "related_process")
