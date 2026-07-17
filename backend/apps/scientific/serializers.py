from rest_framework import serializers

from apps.axes.serializers import ResearchAxisSerializer
from apps.institutional.serializers import InstitutionalUnitSummarySerializer
from apps.scientific.models import ScientificOutput


class ScientificOutputSerializer(serializers.ModelSerializer):
    unit = InstitutionalUnitSummarySerializer(read_only=True, allow_null=True)
    axis = ResearchAxisSerializer(read_only=True)

    class Meta:
        model = ScientificOutput
        fields = (
            "id",
            "unit",
            "title",
            "slug",
            "output_type",
            "axis",
            "authors",
            "abstract",
            "publication_date",
            "file",
            "external_url",
            "published_at",
            "is_featured",
            "display_order",
        )
