from rest_framework import serializers

from apps.institutional.serializers import InstitutionalUnitSummarySerializer
from apps.transparency.models import TransparencyDocument


class TransparencyDocumentSerializer(serializers.ModelSerializer):
    unit = InstitutionalUnitSummarySerializer(read_only=True)

    class Meta:
        model = TransparencyDocument
        fields = (
            "id",
            "unit",
            "title",
            "slug",
            "document_type",
            "description",
            "file",
            "publication_date",
            "related_process",
            "published_at",
        )
