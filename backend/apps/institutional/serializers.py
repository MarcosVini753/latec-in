from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.institutional.models import InstitutionalUnit


class InstitutionalUnitSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionalUnit
        fields = ("name", "acronym", "slug", "unit_type")


class InstitutionalUnitSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    @extend_schema_field(InstitutionalUnitSummarySerializer(allow_null=True))
    def get_parent(self, obj):
        if not obj.parent:
            return None
        return InstitutionalUnitSummarySerializer(obj.parent, context=self.context).data

    class Meta:
        model = InstitutionalUnit
        fields = (
            "id",
            "name",
            "acronym",
            "slug",
            "unit_type",
            "parent",
            "description",
            "mission",
            "vision",
            "logo",
            "cover_image",
            "contact_email",
            "website_url",
            "display_order",
        )
