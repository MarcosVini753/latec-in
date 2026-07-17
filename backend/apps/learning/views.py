from apps.common.viewsets import PublicReadOnlyModelViewSet
from apps.learning.models import Course
from apps.learning.serializers import CourseSerializer


class CourseViewSet(PublicReadOnlyModelViewSet):
    queryset = Course.objects.select_related("unit", "track__unit", "axis__unit").prefetch_related(
        "axis__mentorships__person__role",
        "instructors__role",
        "materials",
    )
    serializer_class = CourseSerializer
    search_fields = ("title", "description")
