# Generated by Django 3.2.13 on 2022-04-23 23:14
import os

import yaml
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations
from nautobot.extras.management import STATUS_COLOR_MAP, STATUS_DESCRIPTION_MAP


def _get_default_status_name():
    return settings.PLUGINS_CONFIG.get("nautobot_firewall_models", {}).get("default_status")


def _get_configured_status_names():
    """Return the configured statuses for the firewall plugin."""
    allowed_statuses = settings.PLUGINS_CONFIG.get("nautobot_firewall_models", {}).get("allowed_status", [])
    default_status = _get_default_status_name()
    configured_statuses = allowed_statuses + [default_status]
    return configured_statuses


def create_configured_statuses(apps):
    """Create the configured statuses for the firewall plugin if they don't already exist."""
    status_names = _get_configured_status_names()
    Status = apps.get_model("extras.Status")
    for status_name in status_names:
        defaults = {"description": STATUS_DESCRIPTION_MAP.get(status_name, "")}
        if status_name in STATUS_COLOR_MAP:
            defaults["color"] = STATUS_COLOR_MAP[status_name]
        Status.objects.get_or_create(name=status_name, defaults=defaults)


def create_status(apps, schema_editor):
    """Initial subset of statuses."""

    create_configured_statuses(apps)
    ContentType = apps.get_model("contenttypes.ContentType")
    Status = apps.get_model("extras.Status")
    status_names = _get_configured_status_names() + ["Active", "Staged", "Decommissioned"]
    for status in Status.objects.filter(name__in=status_names):
        for model in apps.app_configs["nautobot_firewall_models"].get_models():
            if hasattr(model, "status"):
                ct = ContentType.objects.get_for_model(model)
                status.content_types.add(ct)


def reverse_create_status(apps, schema_editor):
    """Remove firewall models from status content_types."""

    ContentType = apps.get_model("contenttypes.ContentType")
    Status = apps.get_model("extras.Status")
    for model in apps.app_configs["nautobot_firewall_models"].get_models():
        content_type = ContentType.objects.get_for_model(model)
        for status in Status.objects.filter(content_types=content_type).iterator():
            status.content_types.remove(content_type)


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


class Migration(migrations.Migration):
    dependencies = [
        ("extras", "0033_add__optimized_indexing"),
        ("nautobot_firewall_models", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(code=create_status, reverse_code=reverse_create_status),
        migrations.RunPython(code=create_default_objects, reverse_code=reverse_create_default_objects),
    ]
