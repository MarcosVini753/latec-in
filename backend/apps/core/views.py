from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.viewsets import PublicReadOnlyModelViewSet
from apps.core.models import HeroBanner, InstitutionalSection, SiteSettings, SocialLink
from apps.core.serializers import (
    HeroBannerSerializer,
    InstitutionalSectionSerializer,
    SiteSettingsSerializer,
    SocialLinkSerializer,
)


class SiteSettingsViewSet(PublicReadOnlyModelViewSet):
    lookup_field = "pk"
    queryset = SiteSettings.objects.select_related("unit").order_by("pk")
    serializer_class = SiteSettingsSerializer


class HomeAPIView(APIView):
    @extend_schema(responses=OpenApiTypes.OBJECT)
    def get(self, request):
        unit_slug = "labtec-in"
        settings = SiteSettings.objects.select_related("unit").filter(is_active=True, unit__slug=unit_slug).first()
        heroes = (
            HeroBanner.objects.select_related("unit")
            .filter(is_published=True, unit__slug=unit_slug)
            .order_by("display_order", "title")
        )
        sections = (
            InstitutionalSection.objects.select_related("unit")
            .filter(is_published=True, unit__slug=unit_slug)
            .order_by("display_order", "title")
        )
        social_links = (
            SocialLink.objects.select_related("unit")
            .filter(is_active=True, unit__slug=unit_slug)
            .order_by("display_order", "label")
        )

        return Response(
            {
                "settings": SiteSettingsSerializer(settings, context={"request": request}).data if settings else None,
                "heroes": HeroBannerSerializer(heroes, many=True, context={"request": request}).data,
                "sections": InstitutionalSectionSerializer(sections, many=True, context={"request": request}).data,
                "social_links": SocialLinkSerializer(social_links, many=True, context={"request": request}).data,
            }
        )
