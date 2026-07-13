from rest_framework import serializers

from apps.axes.serializers import ResearchAxisSerializer
from apps.news.models import Post, PostCategory, Tag
from apps.people.serializers import PersonSerializer


class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ("name", "slug", "description", "display_order")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name", "slug")


class PostSerializer(serializers.ModelSerializer):
    axis = ResearchAxisSerializer(read_only=True)
    category = PostCategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    authors = PersonSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "slug",
            "axis",
            "category",
            "tags",
            "authors",
            "summary",
            "content",
            "cover_image",
            "published_at",
            "is_featured",
            "display_order",
        )
