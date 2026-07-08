from rest_framework import serializers

from apps.core.models import HeroBanner, InstitutionalSection, SiteSettings, SocialLink


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = ("site_name", "description", "institution", "contact_email", "logo")


class HeroBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroBanner
        fields = ("title", "subtitle", "cta_label", "cta_url", "image", "display_order")


class InstitutionalSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionalSection
        fields = ("section_type", "title", "slug", "content", "image", "display_order")


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ("label", "url", "icon", "display_order")
