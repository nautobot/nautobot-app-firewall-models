# Generated by Django 3.2.13 on 2022-05-16 23:54

import django.db.models.deletion
import nautobot.extras.models.statuses
from django.db import migrations

import nautobot_firewall_models.utils


class Migration(migrations.Migration):
    dependencies = [
        ("extras", "0033_add__optimized_indexing"),
        ("nautobot_firewall_models", "0002_custom_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="addressobject",
            name="status",
            field=nautobot.extras.models.statuses.StatusField(
                default=nautobot_firewall_models.utils.get_default_status,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="nautobot_firewall_models_addressobject_related",
                to="extras.status",
            ),
        ),
        migrations.AlterField(
            model_name="addressobjectgroup",
            name="status",
            field=nautobot.extras.models.statuses.StatusField(
                default=nautobot_firewall_models.utils.get_default_status,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="nautobot_firewall_models_addressobjectgroup_related",
                to="extras.status",
            ),
        ),
        migrations.AlterField(
            model_name="fqdn",
            name="status",
            field=nautobot.extras.models.statuses.StatusField(
                default=nautobot_firewall_models.utils.get_default_status,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="nautobot_firewall_models_fqdn_related",
                to="extras.status",
            ),
        ),
        migrations.AlterField(
            model_name="iprange",
            name="status",
            field=nautobot.extras.models.statuses.StatusField(
                default=nautobot_firewall_models.utils.get_default_status,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="nautobot_firewall_models_iprange_related",
                to="extras.status",
            ),
        ),
        migrations.AlterField(
            model_name="policy",
            name="status",
            field=nautobot.extras.models.statuses.StatusField(
                default=nautobot_firewall_models.utils.get_default_status,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="nautobot_firewall_models_policy_related",
                to="extras.status",
            ),
        ),
        migrations.AlterField(
            model_name="policyrule",
            name="status",
            field=nautobot.extras.models.statuses.StatusField(
                default=nautobot_firewall_models.utils.get_default_status,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="nautobot_firewall_models_policyrule_related",
                to="extras.status",
            ),
        ),
        migrations.AlterField(
            model_name="serviceobject",
            name="status",
            field=nautobot.extras.models.statuses.StatusField(
                default=nautobot_firewall_models.utils.get_default_status,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="nautobot_firewall_models_serviceobject_related",
                to="extras.status",
            ),
        ),
        migrations.AlterField(
            model_name="serviceobjectgroup",
            name="status",
            field=nautobot.extras.models.statuses.StatusField(
                default=nautobot_firewall_models.utils.get_default_status,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="nautobot_firewall_models_serviceobjectgroup_related",
                to="extras.status",
            ),
        ),
        migrations.AlterField(
            model_name="userobject",
            name="status",
            field=nautobot.extras.models.statuses.StatusField(
                default=nautobot_firewall_models.utils.get_default_status,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="nautobot_firewall_models_userobject_related",
                to="extras.status",
            ),
        ),
        migrations.AlterField(
            model_name="userobjectgroup",
            name="status",
            field=nautobot.extras.models.statuses.StatusField(
                default=nautobot_firewall_models.utils.get_default_status,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="nautobot_firewall_models_userobjectgroup_related",
                to="extras.status",
            ),
        ),
        migrations.AlterField(
            model_name="zone",
            name="status",
            field=nautobot.extras.models.statuses.StatusField(
                default=nautobot_firewall_models.utils.get_default_status,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="nautobot_firewall_models_zone_related",
                to="extras.status",
            ),
        ),
    ]
