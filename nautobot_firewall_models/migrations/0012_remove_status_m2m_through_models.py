from django.db import migrations


def remove_m2m_through_status_content_types(apps, schema_editor):
    """Remove the through model content types from the Status objects."""

    statuses = ["Active", "Staged", "Decommissioned"]
    ContentType = apps.get_model("contenttypes.ContentType")
    for i in statuses:
        status = apps.get_model("extras.Status").objects.get(name=i)
        for model in apps.app_configs["nautobot_firewall_models"].get_models():
            if not hasattr(model, "status"):
                ct = ContentType.objects.get_for_model(model)
                status.content_types.remove(ct)


class Migration(migrations.Migration):
    dependencies = [
        ("extras", "0033_add__optimized_indexing"),
        ("nautobot_firewall_models", "0011_custom_status_nat"),
    ]

    operations = [
        migrations.RunPython(code=remove_m2m_through_status_content_types, reverse_code=migrations.RunPython.noop),
    ]
