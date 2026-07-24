from django.db.models import Prefetch
from django.db.models import Q
from django.utils import timezone

from apps.common.viewsets import PublicReadOnlyModelViewSet
from apps.institutional.models import InstitutionMembership
from apps.people.models import Person
from apps.people.serializers import PersonSerializer


class PersonViewSet(PublicReadOnlyModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    search_fields = ("full_name", "short_bio")

    def get_queryset(self):
        today = timezone.localdate()
        memberships = InstitutionMembership.objects.filter(
            is_active=True,
            is_public=True,
        ).filter(
            Q(start_date__isnull=True) | Q(start_date__lte=today),
            Q(end_date__isnull=True) | Q(end_date__gte=today),
        ).select_related("unit")
        return super().get_queryset().prefetch_related(
            Prefetch(
                "institution_memberships",
                queryset=memberships,
                to_attr="public_memberships",
            )
        )
