from rest_framework import serializers

from apps.axes.serializers import ResearchAxisSerializer
from apps.institutional.serializers import InstitutionalUnitSummarySerializer
from apps.people.serializers import PersonSerializer
from apps.research.serializers import AcademicWorkSummarySerializer, ResearchProjectSummarySerializer
from apps.scientific.models import ScientificAuthorship, ScientificOutput


class ScientificAuthorshipSerializer(serializers.ModelSerializer):
    person = PersonSerializer(read_only=True)

    class Meta:
        model = ScientificAuthorship
        fields = ("person", "author_order", "author_role")


class ScientificOutputSerializer(serializers.ModelSerializer):
    unit = InstitutionalUnitSummarySerializer(read_only=True, allow_null=True)
    axis = ResearchAxisSerializer(read_only=True)
    research_project = ResearchProjectSummarySerializer(read_only=True, allow_null=True)
    academic_work = AcademicWorkSummarySerializer(read_only=True, allow_null=True)
    authorships = ScientificAuthorshipSerializer(many=True, read_only=True)

    class Meta:
        model = ScientificOutput
        fields = (
            "id",
            "unit",
            "title",
            "slug",
            "output_type",
            "axis",
            "research_project",
            "academic_work",
            "authors",
            "authorships",
            "abstract",
            "publication_date",
            "file",
            "external_url",
            "published_at",
            "is_featured",
            "display_order",
        )
