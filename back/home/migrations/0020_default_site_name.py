from django.db import migrations

SITE_NAME = "Sharks Enlightenment"


def set_default_site_name(apps, schema_editor):
    # The site name is appended to every <title>; an empty one leaves titles like "Home".
    Site = apps.get_model("wagtailcore", "Site")
    Site.objects.filter(site_name="").update(site_name=SITE_NAME)


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0019_footer"),
        ("wagtailcore", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(set_default_site_name, migrations.RunPython.noop),
    ]
