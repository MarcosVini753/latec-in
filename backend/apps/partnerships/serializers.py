from rest_framework import serializers

from apps.partnerships.models import ContactMessage, Partner


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ("id", "name", "slug", "partner_type", "description", "logo", "website", "display_order")


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ("subject", "name", "email", "organization", "message")
