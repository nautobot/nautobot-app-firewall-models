import os

from django.core.exceptions import ObjectDoesNotExist
import yaml


def create_status(apps, schema_editor):
    """Initial subset of statuses."""

    statuses = ["Active", "Staged", "Decommissioned"]
    ContentType = apps.get_model("contenttypes.ContentType")
    for i in statuses:
        status = apps.get_model("extras.Status").objects.get(name=i)
        for model in apps.app_configs["nautobot_firewall_models"].get_models():
            if hasattr(model, "status"):
                ct = ContentType.objects.get_for_model(model)
                status.content_types.add(ct)


def reverse_create_status(apps, schema_editor):
    """Reverse adding firewall models to status content_types."""

    statuses = ["Active", "Staged", "Decommissioned"]
    ContentType = apps.get_model("contenttypes.ContentType")
    for i in statuses:
        status = apps.get_model("extras.Status").objects.get(name=i)
        for model in apps.app_configs["nautobot_firewall_models"].get_models():
            if hasattr(model, "status"):
                ct = ContentType.objects.get_for_model(model)
                status.content_types.remove(ct)


def create_default_objects(apps, schema_editor):
    """Initial subset of commonly used objects."""
    defaults = os.path.join(os.path.dirname(__file__), "services.yml")
    with open(defaults, "r") as f:
        services = yaml.safe_load(f)
    status = apps.get_model("extras.Status").objects.get(name="Active")

    for i in services:
        apps.get_model("nautobot_firewall_models.ServiceObject").objects.create(status=status, **i)


def reverse_create_default_objects(apps, schema_editor):
    """Removes commonly used objects."""
    defaults = os.path.join(os.path.dirname(__file__), "services.yml")
    with open(defaults, "r") as f:
        services = yaml.safe_load(f)
    status = apps.get_model("extras.Status").objects.get(name="Active")

    for i in services:
        try:
            service = apps.get_model("nautobot_firewall_models.ServiceObject").objects.get(status=status, **i)
            service.delete()
        except ObjectDoesNotExist:
            continue


def create_nat_status(apps, schema_editor):
    """Initial subset of statuses for the NAT models.

    This was added along with 0009_nat_policy in order to associate the same set of statuses with the new NAT models
    that are associated with the original set of security models.
    """

    statuses = ["Active", "Staged", "Decommissioned"]
    ContentType = apps.get_model("contenttypes.ContentType")
    relevant_models = [
        apps.get_model(model)
        for model in ["nautobot_firewall_models.NATPolicy", "nautobot_firewall_models.NATPolicyRule"]
    ]
    for i in statuses:
        status = apps.get_model("extras.Status").objects.get(name=i)
        for model in relevant_models:
            ct = ContentType.objects.get_for_model(model)
            status.content_types.add(ct)


def remove_nat_status(apps, schema_editor):
    """Remove status content_type for NAT models.

    This was added along with 0009_nat_policy in order to associate the same set of statuses with the new NAT models
    that are associated with the original set of security models.
    """

    statuses = ["Active", "Staged", "Decommissioned"]
    ContentType = apps.get_model("contenttypes.ContentType")
    relevant_models = [
        apps.get_model(model)
        for model in ["nautobot_firewall_models.NATPolicy", "nautobot_firewall_models.NATPolicyRule"]
    ]
    for i in statuses:
        status = apps.get_model("extras.Status").objects.get(name=i)
        for model in relevant_models:
            ct = ContentType.objects.get_for_model(model)
            status.content_types.remove(ct)
