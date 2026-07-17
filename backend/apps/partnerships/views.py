from rest_framework import mixins, viewsets

from apps.common.viewsets import PublicReadOnlyModelViewSet
from apps.partnerships.models import ContactMessage, Partner
from apps.partnerships.serializers import ContactMessageSerializer, PartnerSerializer


class PartnerViewSet(PublicReadOnlyModelViewSet):
    queryset = Partner.objects.prefetch_related("units")
    serializer_class = PartnerSerializer
    search_fields = ("name", "description")


class ContactMessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ContactMessage.objects.none()
    serializer_class = ContactMessageSerializer
    http_method_names = ["post", "options"]
