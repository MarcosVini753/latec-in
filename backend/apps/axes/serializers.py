from rest_framework import serializers

from apps.axes.models import AxisMentorship, ResearchAxis
from apps.institutional.serializers import InstitutionalUnitSummarySerializer
from apps.people.serializers import PersonSummarySerializer


class AxisMentorshipSerializer(serializers.ModelSerializer):
    person = PersonSummarySerializer(read_only=True)

    class Meta:
        model = AxisMentorship
        fields = ("person", "role", "is_main_mentor", "display_order")


class ResearchAxisSerializer(serializers.ModelSerializer):
    unit = InstitutionalUnitSummarySerializer(read_only=True)
    mentorships = AxisMentorshipSerializer(many=True, read_only=True)

    class Meta:
        model = ResearchAxis
        fields = (
            "id",
            "unit",
            "number",
            "title",
            "slug",
            "description",
            "keywords",
            "display_order",
            "mentorships",
        )
