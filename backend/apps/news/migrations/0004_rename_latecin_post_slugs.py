from django.db import migrations


SLUG_RENAMES = {
    "coordenadora-do-latecin-e-premiada-por-inovacao-tecnologica": (
        "coordenadora-da-latec-e-premiada-por-inovacao-tecnologica"
    ),
    "latecin-participa-do-congresso-nacional-de-inovacao": (
        "latec-participa-do-congresso-nacional-de-inovacao"
    ),
}


def _rename_slugs(apps, schema_editor, renames):
    Post = apps.get_model("news", "Post")
    posts = Post.objects.using(schema_editor.connection.alias)
    changes = []

    for source_slug, destination_slug in renames.items():
        source = posts.filter(slug=source_slug).values("id", "slug").first()
        if source is None:
            continue
        collision = posts.filter(slug=destination_slug).values("id", "slug").first()
        if collision is not None:
            raise RuntimeError(
                "Post slug rename preflight failed: "
                f"source ID {source['id']} ({source_slug}) conflicts with "
                f"destination ID {collision['id']} ({destination_slug})."
            )
        changes.append((source["id"], destination_slug))

    for post_id, destination_slug in changes:
        posts.filter(pk=post_id).update(slug=destination_slug)


def rename_latecin_slugs(apps, schema_editor):
    _rename_slugs(apps, schema_editor, SLUG_RENAMES)


def restore_latecin_slugs(apps, schema_editor):
    _rename_slugs(
        apps,
        schema_editor,
        {destination: source for source, destination in SLUG_RENAMES.items()},
    )


class Migration(migrations.Migration):
    dependencies = [
        ("news", "0003_remove_post_category_remove_post_tags_and_more"),
    ]

    operations = [
        migrations.RunPython(rename_latecin_slugs, restore_latecin_slugs),
    ]
