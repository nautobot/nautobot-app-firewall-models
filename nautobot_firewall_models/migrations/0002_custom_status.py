# Generated by Django 3.2.13 on 2022-04-23 23:14
import os

import yaml
from django.db import migrations

from nautobot_firewall_models.utils import (
    create_configured_statuses,
    get_configured_status_names,
    get_default_status_name,
    get_firewall_models_with_status_field,
)


def create_status(apps, schema_editor):
    """Initial subset of statuses."""

    create_configured_statuses(apps)

    content_types = get_firewall_models_with_status_field(apps)
    Status = apps.get_model("extras.Status")
    status_names = get_configured_status_names()
    for status in Status.objects.filter(name__in=status_names).iterator():
        status.content_types.add(*content_types)


def reverse_create_status(apps, schema_editor):
    """Remove firewall models from status content_types."""

    ContentType = apps.get_model("contenttypes.ContentType")
    Status = apps.get_model("extras.Status")
    firewall_models_content_types = ContentType.objects.filter(app_label="nautobot_firewall_models")
    for status in Status.objects.filter(content_types__in=firewall_models_content_types).distinct().iterator():
        status.content_types.remove(*firewall_models_content_types)


def create_default_objects(apps, schema_editor):
    """Initial subset of commonly used objects."""
    default_services_file = os.path.join(os.path.dirname(__file__), "services.yml")
    Status = apps.get_model("extras.Status")
    ServiceObject = apps.get_model("nautobot_firewall_models.ServiceObject")
    default_status = Status.objects.get(name=get_default_status_name())

    with open(default_services_file, "r") as f:
        default_services = yaml.safe_load(f)

    for service in default_services:
        ServiceObject.objects.create(status=default_status, **service)


def reverse_create_default_objects(apps, schema_editor):
    """
    Removes commonly used objects.

    Currently skipped due to Django bug https://code.djangoproject.com/ticket/33586
    """
    default_services_file = os.path.join(os.path.dirname(__file__), "services.yml")
    ServiceObject = apps.get_model("nautobot_firewall_models.ServiceObject")

    with open(default_services_file, "r") as f:
        default_services = yaml.safe_load(f)

    for service in default_services:
        ServiceObject.objects.filter(**service).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("extras", "0033_add__optimized_indexing"),
        ("nautobot_firewall_models", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(code=create_status, reverse_code=reverse_create_status),
        migrations.RunPython(code=create_default_objects, reverse_code=migrations.RunPython.noop),
    ]
