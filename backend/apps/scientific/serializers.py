from rest_framework import serializers

from apps.axes.serializers import ResearchAxisSerializer
from apps.scientific.models import ScientificOutput


class ScientificOutputSerializer(serializers.ModelSerializer):
    axis = ResearchAxisSerializer(read_only=True)

    class Meta:
        model = ScientificOutput
        fields = (
            "id",
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
