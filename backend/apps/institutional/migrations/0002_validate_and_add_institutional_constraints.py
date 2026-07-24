from django.db import migrations, models
from django.db.models import F, Q


def validate_existing_institutional_data(apps, schema_editor):
    Membership = apps.get_model("institutional", "InstitutionMembership")
    Unit = apps.get_model("institutional", "InstitutionalUnit")

    duplicate_ids = set()
    invalid_date_ids = []
    membership_by_key = {}
    for membership_id, person_id, unit_id, role, start_date, end_date in Membership.objects.values_list(
        "id", "person_id", "unit_id", "role", "start_date", "end_date"
    ):
        key = (person_id, unit_id, role)
        previous_id = membership_by_key.setdefault(key, membership_id)
        if previous_id != membership_id:
            duplicate_ids.update((previous_id, membership_id))
        if start_date and end_date and end_date < start_date:
            invalid_date_ids.append(membership_id)

    parent_by_unit = dict(Unit.objects.values_list("id", "parent_id"))
    cycle_ids = set()
    for unit_id in parent_by_unit:
        path = []
        position_by_id = {}
        ancestor_id = unit_id
        while ancestor_id is not None and ancestor_id in parent_by_unit:
            if ancestor_id in position_by_id:
                cycle_ids.update(path[position_by_id[ancestor_id] :])
                break
            position_by_id[ancestor_id] = len(path)
            path.append(ancestor_id)
            ancestor_id = parent_by_unit[ancestor_id]

    issues = []
    if duplicate_ids:
        issues.append(f"duplicate InstitutionMembership IDs: {sorted(duplicate_ids)}")
    if invalid_date_ids:
        issues.append(f"invalid InstitutionMembership date-range IDs: {sorted(invalid_date_ids)}")
    if cycle_ids:
        issues.append(f"cyclic InstitutionalUnit IDs: {sorted(cycle_ids)}")
    if issues:
        raise RuntimeError("Institutional constraint preflight failed: " + "; ".join(issues))


class Migration(migrations.Migration):
    dependencies = [
        ("institutional", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(validate_existing_institutional_data, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name="institutionalunit",
            constraint=models.CheckConstraint(
                check=~Q(parent=F("id")),
                name="institutional_unit_parent_not_self",
            ),
        ),
        migrations.AddConstraint(
            model_name="institutionmembership",
            constraint=models.UniqueConstraint(
                fields=("person", "unit", "role"),
                name="unique_institution_membership",
            ),
        ),
        migrations.AddConstraint(
            model_name="institutionmembership",
            constraint=models.CheckConstraint(
                check=(
                    Q(start_date__isnull=True)
                    | Q(end_date__isnull=True)
                    | Q(end_date__gte=F("start_date"))
                ),
                name="valid_membership_date_range",
            ),
        ),
    ]
