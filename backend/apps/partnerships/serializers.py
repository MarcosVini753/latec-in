from rest_framework import serializers

from apps.institutional.serializers import InstitutionalUnitSummarySerializer
from apps.partnerships.models import ContactMessage, Partner


class PartnerSerializer(serializers.ModelSerializer):
    units = InstitutionalUnitSummarySerializer(many=True, read_only=True)

    class Meta:
        model = Partner
        fields = ("id", "units", "name", "slug", "partner_type", "description", "logo", "website", "display_order")


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ("contact_type", "subject", "name", "email", "organization", "message")
