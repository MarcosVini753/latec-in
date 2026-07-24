from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("learning", "0004_remove_learningtrack_unit_remove_course_track_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="coursematerial",
            name="is_public",
        ),
    ]
