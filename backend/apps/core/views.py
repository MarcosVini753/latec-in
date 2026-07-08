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
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer


class HomeAPIView(APIView):
    @extend_schema(responses=OpenApiTypes.OBJECT)
    def get(self, request):
        settings = SiteSettings.objects.filter(is_active=True).first()
        heroes = HeroBanner.objects.filter(is_published=True).order_by("display_order", "title")
        sections = InstitutionalSection.objects.filter(is_published=True).order_by("display_order", "title")
        social_links = SocialLink.objects.filter(is_active=True).order_by("display_order", "label")

        return Response(
            {
                "settings": SiteSettingsSerializer(settings, context={"request": request}).data if settings else None,
                "heroes": HeroBannerSerializer(heroes, many=True, context={"request": request}).data,
                "sections": InstitutionalSectionSerializer(sections, many=True, context={"request": request}).data,
                "social_links": SocialLinkSerializer(social_links, many=True, context={"request": request}).data,
            }
        )
