from rest_framework import serializers

from apps.core.models import HeroBanner, InstitutionalSection, SiteSettings, SocialLink
from apps.institutional.serializers import InstitutionalUnitSummarySerializer


class SiteSettingsSerializer(serializers.ModelSerializer):
    unit = InstitutionalUnitSummarySerializer(read_only=True)

    class Meta:
        model = SiteSettings
        fields = ("unit", "site_name", "description", "institution", "contact_email", "logo")


class HeroBannerSerializer(serializers.ModelSerializer):
    unit = InstitutionalUnitSummarySerializer(read_only=True)

    class Meta:
        model = HeroBanner
        fields = ("unit", "title", "subtitle", "cta_label", "cta_url", "image", "display_order")


class InstitutionalSectionSerializer(serializers.ModelSerializer):
    unit = InstitutionalUnitSummarySerializer(read_only=True)

    class Meta:
        model = InstitutionalSection
        fields = ("unit", "section_type", "title", "slug", "content", "image", "display_order")


class SocialLinkSerializer(serializers.ModelSerializer):
    unit = InstitutionalUnitSummarySerializer(read_only=True)

    class Meta:
        model = SocialLink
        fields = ("unit", "label", "url", "icon", "display_order")
