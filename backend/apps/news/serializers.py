from rest_framework import serializers

from apps.axes.serializers import ResearchAxisSerializer
from apps.institutional.serializers import InstitutionalUnitSummarySerializer
from apps.news.models import Post


class PostSerializer(serializers.ModelSerializer):
    unit = InstitutionalUnitSummarySerializer(read_only=True)
    axis = ResearchAxisSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "unit",
            "title",
            "slug",
            "axis",
            "summary",
            "content",
            "cover_image",
            "published_at",
        )
