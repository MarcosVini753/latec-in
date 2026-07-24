from django.db import migrations


def drop_legacy_mediahub(apps, schema_editor):
    table_name = schema_editor.quote_name("mediahub_mediaasset")
    schema_editor.execute(f"DROP TABLE IF EXISTS {table_name}")

    ContentType = apps.get_model("contenttypes", "ContentType")
    ContentType.objects.using(schema_editor.connection.alias).filter(
        app_label="mediahub"
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("research", "0004_alter_academicwork_options_and_more"),
    ]

    operations = [
        migrations.RunPython(drop_legacy_mediahub, migrations.RunPython.noop),
    ]
