# Copied on 2022-09-23 10:57

from django.db import migrations


def create_nat_status(apps, schema_editor):
    """Initial subset of statuses for the NAT models.

    This was added along with 0009_nat_policy in order to associate the same set of statuses with the new NAT models
    that are associated with the original set of security models.
    """

    statuses = ["active", "staged", "decommissioned"]
    ContentType = apps.get_model("contenttypes.ContentType")
    relevant_models = [
        apps.get_model(model)
        for model in ["nautobot_firewall_models.NATPolicy", "nautobot_firewall_models.NATPolicyRule"]
    ]
    for i in statuses:
        status = apps.get_model("extras.Status").objects.get(slug=i)
        for model in relevant_models:
            ct = ContentType.objects.get_for_model(model)
            status.content_types.add(ct)

def remove_nat_status(apps, schema_editor):
    """Remove status content_type for NAT models.

    This was added along with 0009_nat_policy in order to associate the same set of statuses with the new NAT models
    that are associated with the original set of security models.
    """

    statuses = ["active", "staged", "decommissioned"]
    ContentType = apps.get_model("contenttypes.ContentType")
    relevant_models = [
        apps.get_model(model)
        for model in ["nautobot_firewall_models.NATPolicy", "nautobot_firewall_models.NATPolicyRule"]
    ]
    for i in statuses:
        status = apps.get_model("extras.Status").objects.get(slug=i)
        for model in relevant_models:
            ct = ContentType.objects.get_for_model(model)
            status.content_types.remove(ct)

class Migration(migrations.Migration):

    dependencies = [
        ("extras", "0033_add__optimized_indexing"),
        ("nautobot_firewall_models", "0010_nat_policy"),
    ]

    operations = [
        migrations.RunPython(code=create_nat_status, reverse_code=remove_nat_status),
    ]
