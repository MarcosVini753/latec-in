from rest_framework import serializers

from apps.axes.serializers import ResearchAxisSerializer
from apps.institutional.serializers import InstitutionalUnitSummarySerializer
from apps.people.serializers import PersonSummarySerializer
from apps.research.models import AcademicWork, AcademicWorkContributor, ResearchProject, ResearchProjectMember


class ResearchProjectSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchProject
        fields = ("id", "title", "slug", "project_status")


class ResearchProjectMemberSerializer(serializers.ModelSerializer):
    person = PersonSummarySerializer(read_only=True)

    class Meta:
        model = ResearchProjectMember
        fields = ("person", "role", "display_order")


class ResearchProjectSerializer(serializers.ModelSerializer):
    unit = InstitutionalUnitSummarySerializer(read_only=True)
    axis = ResearchAxisSerializer(read_only=True, allow_null=True)
    team_members = ResearchProjectMemberSerializer(many=True, read_only=True)

    class Meta:
        model = ResearchProject
        fields = (
            "id",
            "unit",
            "axis",
            "title",
            "slug",
            "summary",
            "file",
            "external_url",
            "start_date",
            "end_date",
            "project_status",
            "published_at",
            "team_members",
        )


class AcademicWorkSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicWork
        fields = ("id", "title", "slug", "work_type", "year")


class AcademicWorkContributorSerializer(serializers.ModelSerializer):
    person = PersonSummarySerializer(read_only=True)

    class Meta:
        model = AcademicWorkContributor
        fields = ("person", "role", "display_order")


class AcademicWorkSerializer(serializers.ModelSerializer):
    unit = InstitutionalUnitSummarySerializer(read_only=True)
    research_project = ResearchProjectSummarySerializer(read_only=True, allow_null=True)
    contributors = AcademicWorkContributorSerializer(source="work_contributors", many=True, read_only=True)

    class Meta:
        model = AcademicWork
        fields = (
            "id",
            "unit",
            "research_project",
            "title",
            "slug",
            "work_type",
            "course",
            "institution",
            "year",
            "abstract",
            "keywords",
            "file",
            "external_url",
            "published_at",
            "contributors",
        )
