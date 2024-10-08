from django.db import migrations


def remove_m2m_through_status_content_types(apps, schema_editor):
    """Remove the through model content types from the Status objects."""

    ContentType = apps.get_model("contenttypes.ContentType")
    Status = apps.get_model("extras.Status")
    firewall_models_without_status_field = []
    for model in apps.app_configs["nautobot_firewall_models"].get_models():
        if not hasattr(model, "status"):
            ct = ContentType.objects.get_for_model(model)
            firewall_models_without_status_field.append(ct)
    for status in Status.objects.filter(content_types__in=firewall_models_without_status_field).distinct().iterator():
        status.content_types.remove(*firewall_models_without_status_field)


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("extras", "0033_add__optimized_indexing"),
        ("nautobot_firewall_models", "0011_custom_status_nat"),
    ]

    operations = [
        migrations.RunPython(code=remove_m2m_through_status_content_types, reverse_code=migrations.RunPython.noop),
    ]
