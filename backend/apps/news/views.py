from apps.common.viewsets import PublicReadOnlyModelViewSet
from apps.news.models import Post, Tag
from apps.news.serializers import PostSerializer, TagSerializer


class PostTagViewSet(PublicReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    search_fields = ("name",)


class PostViewSet(PublicReadOnlyModelViewSet):
    queryset = Post.objects.select_related("unit", "axis__unit", "category").prefetch_related(
        "axis__mentorships__person__role",
        "tags",
        "authors__role",
    )
    serializer_class = PostSerializer
    search_fields = ("title", "summary", "content")
