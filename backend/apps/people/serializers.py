from rest_framework import serializers

from apps.people.models import Person, Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("name", "slug", "description", "display_order")


class PersonSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)

    class Meta:
        model = Person
        fields = (
            "id",
            "full_name",
            "slug",
            "role",
            "short_bio",
            "photo",
            "email",
            "lattes_url",
            "linkedin_url",
            "website_url",
            "is_featured",
            "display_order",
        )
