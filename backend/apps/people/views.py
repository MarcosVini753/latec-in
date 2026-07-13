from apps.common.viewsets import PublicReadOnlyModelViewSet
from apps.people.models import Person
from apps.people.serializers import PersonSerializer


class PersonViewSet(PublicReadOnlyModelViewSet):
    queryset = Person.objects.select_related("role").all()
    serializer_class = PersonSerializer
    search_fields = ("full_name", "short_bio")
