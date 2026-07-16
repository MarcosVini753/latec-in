from apps.common.viewsets import PublicReadOnlyModelViewSet
from apps.institutional.models import InstitutionalUnit
from apps.institutional.serializers import InstitutionalUnitSerializer


class InstitutionalUnitViewSet(PublicReadOnlyModelViewSet):
    queryset = InstitutionalUnit.objects.filter(is_public=True).select_related("parent")
    serializer_class = InstitutionalUnitSerializer
    search_fields = ("name", "acronym", "description")
