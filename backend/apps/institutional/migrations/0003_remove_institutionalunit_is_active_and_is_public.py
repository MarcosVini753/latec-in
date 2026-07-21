from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("institutional", "0002_validate_and_add_institutional_constraints"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="institutionalunit",
            name="is_active",
        ),
        migrations.RemoveField(
            model_name="institutionalunit",
            name="is_public",
        ),
    ]
