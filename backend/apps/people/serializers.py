from drf_spectacular.utils import extend_schema_field
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from apps.institutional.models import InstitutionMembership
from apps.institutional.serializers import InstitutionalUnitSummarySerializer
from apps.people.models import Person


class PersonMembershipSerializer(serializers.ModelSerializer):
    unit = InstitutionalUnitSummarySerializer(read_only=True)

    class Meta:
        model = InstitutionMembership
        fields = ("unit", "role")


class PersonSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ("id", "full_name", "slug", "photo")


class PersonSerializer(serializers.ModelSerializer):
    memberships = serializers.SerializerMethodField()

    @extend_schema_field(PersonMembershipSerializer(many=True))
    def get_memberships(self, obj):
        memberships = getattr(obj, "public_memberships", None)
        if memberships is None:
            today = timezone.localdate()
            memberships = obj.institution_memberships.filter(
                is_active=True,
                is_public=True,
            ).filter(
                Q(start_date__isnull=True) | Q(start_date__lte=today),
                Q(end_date__isnull=True) | Q(end_date__gte=today),
            ).select_related("unit")
        return PersonMembershipSerializer(memberships, many=True, context=self.context).data

    class Meta:
        model = Person
        fields = (
            "id",
            "full_name",
            "slug",
            "memberships",
            "short_bio",
            "photo",
            "email",
            "lattes_url",
            "linkedin_url",
            "website_url",
            "display_order",
        )
