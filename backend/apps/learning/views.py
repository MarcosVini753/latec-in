from apps.common.viewsets import PublicReadOnlyModelViewSet
from apps.learning.models import Course
from apps.learning.serializers import CourseSerializer


class CourseViewSet(PublicReadOnlyModelViewSet):
    queryset = Course.objects.select_related("track", "axis").prefetch_related("instructors__role", "materials").all()
    serializer_class = CourseSerializer
    search_fields = ("title", "description")
