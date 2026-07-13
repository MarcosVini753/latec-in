from rest_framework import serializers

from apps.transparency.models import TransparencyDocument


class TransparencyDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransparencyDocument
        fields = (
            "id",
            "title",
            "slug",
            "document_type",
            "description",
            "file",
            "publication_date",
            "related_process",
            "published_at",
            "is_featured",
            "display_order",
        )
