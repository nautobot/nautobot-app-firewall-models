# Copied on 2022-11-18

from django.db import migrations


def create_app_status(apps, schema_editor):
    """Initial subset of statuses for the Application models.

    This was added along with 0013_applications in order to associate the same set of statuses with the new Application models
    that are associated with the original set of security models.
    """

    statuses = ["active", "staged", "decommissioned"]
    ContentType = apps.get_model("contenttypes.ContentType")
    relevant_models = [
        apps.get_model(model)
        for model in ["nautobot_firewall_models.ApplicationObject", "nautobot_firewall_models.ApplicationObjectGroup"]
    ]
    for i in statuses:
        status = apps.get_model("extras.Status").objects.get(slug=i)
        for model in relevant_models:
            ct = ContentType.objects.get_for_model(model)
            status.content_types.add(ct)


def remove_app_status(apps, schema_editor):
    """Remove status content_type for Application models.

    This was added along with 0013_applications in order to associate the same set of statuses with the new Application models
    that are associated with the original set of security models.
    """

    statuses = ["active", "staged", "decommissioned"]
    ContentType = apps.get_model("contenttypes.ContentType")
    relevant_models = [
        apps.get_model(model)
        for model in ["nautobot_firewall_models.ApplicationObject", "nautobot_firewall_models.ApplicationObjectGroup"]
    ]
    for i in statuses:
        status = apps.get_model("extras.Status").objects.get(slug=i)
        for model in relevant_models:
            ct = ContentType.objects.get_for_model(model)
            status.content_types.remove(ct)


class Migration(migrations.Migration):

    dependencies = [
        ("nautobot_firewall_models", "0013_applications"),
    ]

    operations = [
        migrations.RunPython(code=create_app_status, reverse_code=remove_app_status),
    ]
