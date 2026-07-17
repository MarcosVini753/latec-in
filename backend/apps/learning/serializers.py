from rest_framework import serializers

from apps.axes.serializers import ResearchAxisSerializer
from apps.institutional.serializers import InstitutionalUnitSummarySerializer
from apps.learning.models import Course, CourseMaterial, LearningTrack
from apps.people.serializers import PersonSerializer


class LearningTrackSerializer(serializers.ModelSerializer):
    unit = InstitutionalUnitSummarySerializer(read_only=True, allow_null=True)

    class Meta:
        model = LearningTrack
        fields = ("unit", "title", "slug", "description", "display_order")


class CourseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMaterial
        fields = ("title", "description", "file", "external_url", "display_order")


class CourseSerializer(serializers.ModelSerializer):
    unit = InstitutionalUnitSummarySerializer(read_only=True, allow_null=True)
    track = LearningTrackSerializer(read_only=True)
    axis = ResearchAxisSerializer(read_only=True)
    instructors = PersonSerializer(many=True, read_only=True)
    materials = CourseMaterialSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "unit",
            "title",
            "slug",
            "track",
            "axis",
            "instructors",
            "description",
            "start_date",
            "end_date",
            "workload_hours",
            "enrollment_status",
            "registration_url",
            "cover_image",
            "published_at",
            "is_featured",
            "display_order",
            "materials",
        )
