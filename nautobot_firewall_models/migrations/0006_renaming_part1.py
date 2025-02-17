# Generated by Django 3.2.15 on 2022-08-26 18:03

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("nautobot_firewall_models", "0005_capircapolicy"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="SvcGroupM2M",
            new_name="DestSvcGroupM2M",
        ),
        migrations.RenameModel(
            old_name="SvcM2M",
            new_name="DestSvcM2M",
        ),
        migrations.RenameField(
            model_name="policyrule",
            old_name="destination_address_group",
            new_name="destination_address_groups",
        ),
        migrations.RenameField(
            model_name="policyrule",
            old_name="destination_address",
            new_name="destination_addresses",
        ),
        migrations.RenameField(
            model_name="policyrule",
            old_name="source_address_group",
            new_name="source_address_groups",
        ),
        migrations.RenameField(
            model_name="policyrule",
            old_name="source_address",
            new_name="source_addresses",
        ),
        migrations.RenameField(
            model_name="policyrule",
            old_name="source_user_group",
            new_name="source_user_groups",
        ),
        migrations.RenameField(
            model_name="policyrule",
            old_name="source_user",
            new_name="source_users",
        ),
        migrations.RemoveField(
            model_name="policyrule",
            name="service",
        ),
        migrations.RemoveField(
            model_name="policyrule",
            name="service_group",
        ),
        migrations.AddField(
            model_name="policyrule",
            name="destination_service_groups",
            field=models.ManyToManyField(
                related_name="destination_policy_rules",
                through="nautobot_firewall_models.DestSvcGroupM2M",
                to="nautobot_firewall_models.ServiceObjectGroup",
            ),
        ),
        migrations.AddField(
            model_name="policyrule",
            name="destination_services",
            field=models.ManyToManyField(
                related_name="destination_policy_rules",
                through="nautobot_firewall_models.DestSvcM2M",
                to="nautobot_firewall_models.ServiceObject",
            ),
        ),
        migrations.AddField(
            model_name="policyrule",
            name="index",
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name="SrcSvcM2M",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "pol_rule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="nautobot_firewall_models.policyrule"
                    ),
                ),
                (
                    "svc",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="nautobot_firewall_models.serviceobject"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="SrcSvcGroupM2M",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "pol_rule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="nautobot_firewall_models.policyrule"
                    ),
                ),
                (
                    "svc_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="nautobot_firewall_models.serviceobjectgroup"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="policyrule",
            name="source_service_groups",
            field=models.ManyToManyField(
                related_name="source_policy_rules",
                through="nautobot_firewall_models.SrcSvcGroupM2M",
                to="nautobot_firewall_models.ServiceObjectGroup",
            ),
        ),
        migrations.AddField(
            model_name="policyrule",
            name="source_services",
            field=models.ManyToManyField(
                related_name="source_policy_rules",
                through="nautobot_firewall_models.SrcSvcM2M",
                to="nautobot_firewall_models.ServiceObject",
            ),
        ),
    ]
