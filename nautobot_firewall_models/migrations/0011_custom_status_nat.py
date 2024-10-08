# Copied on 2022-09-23 10:57

from django.db import migrations

from nautobot_firewall_models.utils import create_configured_statuses, get_configured_status_names


def create_nat_status(apps, schema_editor):
    """Initial subset of statuses for the NAT models.

    This was added along with 0009_nat_policy in order to associate the same set of statuses with the new NAT models
    that are associated with the original set of security models.
    """
    create_configured_statuses(apps)

    ContentType = apps.get_model("contenttypes.ContentType")
    Status = apps.get_model("extras.Status")
    relevant_models_ct = ContentType.objects.filter(
        app_label="nautobot_firewall_models", model__in=["natpolicy", "natpolicyrule"]
    )
    for status in Status.objects.filter(name__in=get_configured_status_names()).iterator():
        status.content_types.add(*relevant_models_ct)


def remove_nat_status(apps, schema_editor):
    """Remove status content_type for NAT models.

    This was added along with 0009_nat_policy in order to associate the same set of statuses with the new NAT models
    that are associated with the original set of security models.
    """

    ContentType = apps.get_model("contenttypes.ContentType")
    Status = apps.get_model("extras.Status")
    relevant_models_ct = ContentType.objects.filter(
        app_label="nautobot_firewall_models", model__in=["natpolicy", "natpolicyrule"]
    )
    for status in Status.objects.filter(content_types__in=relevant_models_ct).distinct().iterator():
        status.content_types.remove(*relevant_models_ct)


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("extras", "0033_add__optimized_indexing"),
        ("nautobot_firewall_models", "0010_nat_policy"),
    ]

    operations = [
        migrations.RunPython(code=create_nat_status, reverse_code=remove_nat_status),
    ]
