# Generated by Django 3.2.15 on 2022-09-28 11:31

import uuid

import django.core.serializers.json
import django.db.models.deletion
import nautobot.extras.models.mixins
import nautobot.extras.models.statuses
import taggit.managers
from django.db import migrations, models

import nautobot_firewall_models.utils


class Migration(migrations.Migration):
    dependencies = [
        ("extras", "0047_enforce_custom_field_slug"),
        ("tenancy", "0002_auto_slug"),
        ("dcim", "0014_location_status_data_migration"),
        ("nautobot_firewall_models", "0009_proper_ordering_on_through"),
    ]

    operations = [
        migrations.CreateModel(
            name="NATOrigDestAddrGroupM2M",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "addr_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="nautobot_firewall_models.addressobjectgroup"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="NATOrigDestAddrM2M",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="NATOrigDestSvcGroupM2M",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="NATOrigDestSvcM2M",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="NATOrigSrcAddrGroupM2M",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "addr_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="nautobot_firewall_models.addressobjectgroup"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="NATOrigSrcAddrM2M",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "addr",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="nautobot_firewall_models.addressobject"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="NATOrigSrcSvcGroupM2M",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="NATOrigSrcSvcM2M",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="NATPolicy",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "_custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder),
                ),
                ("description", models.CharField(blank=True, max_length=200)),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
            options={
                "verbose_name_plural": "NAT Policies",
                "ordering": ["name"],
            },
            bases=(
                models.Model,
                nautobot.extras.models.mixins.DynamicGroupMixin,
                nautobot.extras.models.mixins.NotesMixin,
            ),
        ),
        migrations.CreateModel(
            name="NATPolicyRule",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "_custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder),
                ),
                ("name", models.CharField(max_length=100)),
                ("remark", models.BooleanField(default=False)),
                ("log", models.BooleanField(default=False)),
                ("request_id", models.CharField(blank=True, max_length=100, null=True)),
                ("description", models.CharField(blank=True, max_length=200, null=True)),
                ("index", models.PositiveSmallIntegerField(blank=True, null=True)),
                (
                    "destination_zone",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="destination_nat_policy_rules",
                        to="nautobot_firewall_models.zone",
                    ),
                ),
                (
                    "original_destination_address_groups",
                    models.ManyToManyField(
                        related_name="original_destination_nat_policy_rules",
                        through="nautobot_firewall_models.NATOrigDestAddrGroupM2M",
                        to="nautobot_firewall_models.AddressObjectGroup",
                    ),
                ),
                (
                    "original_destination_addresses",
                    models.ManyToManyField(
                        related_name="original_destination_nat_policy_rules",
                        through="nautobot_firewall_models.NATOrigDestAddrM2M",
                        to="nautobot_firewall_models.AddressObject",
                    ),
                ),
                (
                    "original_destination_service_groups",
                    models.ManyToManyField(
                        related_name="original_destination_nat_policy_rules",
                        through="nautobot_firewall_models.NATOrigDestSvcGroupM2M",
                        to="nautobot_firewall_models.ServiceObjectGroup",
                    ),
                ),
                (
                    "original_destination_services",
                    models.ManyToManyField(
                        related_name="original_destination_nat_policy_rules",
                        through="nautobot_firewall_models.NATOrigDestSvcM2M",
                        to="nautobot_firewall_models.ServiceObject",
                    ),
                ),
                (
                    "original_source_address_groups",
                    models.ManyToManyField(
                        related_name="original_source_nat_policy_rules",
                        through="nautobot_firewall_models.NATOrigSrcAddrGroupM2M",
                        to="nautobot_firewall_models.AddressObjectGroup",
                    ),
                ),
                (
                    "original_source_addresses",
                    models.ManyToManyField(
                        related_name="original_source_nat_policy_rules",
                        through="nautobot_firewall_models.NATOrigSrcAddrM2M",
                        to="nautobot_firewall_models.AddressObject",
                    ),
                ),
                (
                    "original_source_service_groups",
                    models.ManyToManyField(
                        related_name="original_source_nat_policy_rules",
                        through="nautobot_firewall_models.NATOrigSrcSvcGroupM2M",
                        to="nautobot_firewall_models.ServiceObjectGroup",
                    ),
                ),
                (
                    "original_source_services",
                    models.ManyToManyField(
                        related_name="original_source_nat_policy_rules",
                        through="nautobot_firewall_models.NATOrigSrcSvcM2M",
                        to="nautobot_firewall_models.ServiceObject",
                    ),
                ),
                (
                    "source_zone",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="source_nat_policy_rules",
                        to="nautobot_firewall_models.zone",
                    ),
                ),
                (
                    "status",
                    nautobot.extras.models.statuses.StatusField(
                        default=nautobot_firewall_models.utils.get_default_status,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="nautobot_firewall_models_natpolicyrule_related",
                        to="extras.status",
                    ),
                ),
                ("tags", taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag")),
            ],
            options={
                "verbose_name_plural": "NAT Policy Rules",
                "ordering": ["index"],
            },
            bases=(
                models.Model,
                nautobot.extras.models.mixins.DynamicGroupMixin,
                nautobot.extras.models.mixins.NotesMixin,
            ),
        ),
        migrations.CreateModel(
            name="NATTransSrcSvcM2M",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "nat_pol_rule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="nautobot_firewall_models.natpolicyrule"
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
            name="NATTransSrcSvcGroupM2M",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "nat_pol_rule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="nautobot_firewall_models.natpolicyrule"
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
        migrations.CreateModel(
            name="NATTransSrcAddrM2M",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "addr",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="nautobot_firewall_models.addressobject"
                    ),
                ),
                (
                    "nat_pol_rule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="nautobot_firewall_models.natpolicyrule"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="NATTransSrcAddrGroupM2M",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "addr_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="nautobot_firewall_models.addressobjectgroup"
                    ),
                ),
                (
                    "nat_pol_rule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="nautobot_firewall_models.natpolicyrule"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="NATTransDestSvcM2M",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "nat_pol_rule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="nautobot_firewall_models.natpolicyrule"
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
            name="NATTransDestSvcGroupM2M",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "nat_pol_rule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="nautobot_firewall_models.natpolicyrule"
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
        migrations.CreateModel(
            name="NATTransDestAddrM2M",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "nat_pol_rule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="nautobot_firewall_models.natpolicyrule"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="nautobot_firewall_models.addressobject"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="NATTransDestAddrGroupM2M",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "addr_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="nautobot_firewall_models.addressobjectgroup"
                    ),
                ),
                (
                    "nat_pol_rule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="nautobot_firewall_models.natpolicyrule"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="NATSrcUserM2M",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "nat_pol_rule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="nautobot_firewall_models.natpolicyrule"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="nautobot_firewall_models.userobject"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="NATSrcUserGroupM2M",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "nat_pol_rule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="nautobot_firewall_models.natpolicyrule"
                    ),
                ),
                (
                    "user_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="nautobot_firewall_models.userobjectgroup"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="NATPolicyRuleM2M",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "nat_policy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="nautobot_firewall_models.natpolicy"
                    ),
                ),
                (
                    "nat_rule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="nautobot_firewall_models.natpolicyrule"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="natpolicyrule",
            name="translated_destination_address_groups",
            field=models.ManyToManyField(
                related_name="translated_destination_nat_policy_rules",
                through="nautobot_firewall_models.NATTransDestAddrGroupM2M",
                to="nautobot_firewall_models.AddressObjectGroup",
            ),
        ),
        migrations.AddField(
            model_name="natpolicyrule",
            name="translated_destination_addresses",
            field=models.ManyToManyField(
                related_name="translated_destination_nat_policy_rules",
                through="nautobot_firewall_models.NATTransDestAddrM2M",
                to="nautobot_firewall_models.AddressObject",
            ),
        ),
        migrations.AddField(
            model_name="natpolicyrule",
            name="translated_destination_service_groups",
            field=models.ManyToManyField(
                related_name="translated_destination_nat_policy_rules",
                through="nautobot_firewall_models.NATTransDestSvcGroupM2M",
                to="nautobot_firewall_models.ServiceObjectGroup",
            ),
        ),
        migrations.AddField(
            model_name="natpolicyrule",
            name="translated_destination_services",
            field=models.ManyToManyField(
                related_name="translated_destination_nat_policy_rules",
                through="nautobot_firewall_models.NATTransDestSvcM2M",
                to="nautobot_firewall_models.ServiceObject",
            ),
        ),
        migrations.AddField(
            model_name="natpolicyrule",
            name="translated_source_address_groups",
            field=models.ManyToManyField(
                related_name="translated_source_nat_policy_rules",
                through="nautobot_firewall_models.NATTransSrcAddrGroupM2M",
                to="nautobot_firewall_models.AddressObjectGroup",
            ),
        ),
        migrations.AddField(
            model_name="natpolicyrule",
            name="translated_source_addresses",
            field=models.ManyToManyField(
                related_name="translated_source_nat_policy_rules",
                through="nautobot_firewall_models.NATTransSrcAddrM2M",
                to="nautobot_firewall_models.AddressObject",
            ),
        ),
        migrations.AddField(
            model_name="natpolicyrule",
            name="translated_source_service_groups",
            field=models.ManyToManyField(
                related_name="translated_source_nat_policy_rules",
                through="nautobot_firewall_models.NATTransSrcSvcGroupM2M",
                to="nautobot_firewall_models.ServiceObjectGroup",
            ),
        ),
        migrations.AddField(
            model_name="natpolicyrule",
            name="translated_source_services",
            field=models.ManyToManyField(
                related_name="translated_source_nat_policy_rules",
                through="nautobot_firewall_models.NATTransSrcSvcM2M",
                to="nautobot_firewall_models.ServiceObject",
            ),
        ),
        migrations.CreateModel(
            name="NATPolicyNATRuleM2M",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "nat_policy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="nautobot_firewall_models.natpolicy"
                    ),
                ),
                (
                    "nat_rule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="nautobot_firewall_models.natpolicyrule"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="NATPolicyDynamicGroupM2M",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("weight", models.PositiveSmallIntegerField(default=100)),
                (
                    "dynamic_group",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="extras.dynamicgroup"),
                ),
                (
                    "nat_policy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="nautobot_firewall_models.natpolicy"
                    ),
                ),
            ],
            options={
                "ordering": ["weight"],
                "unique_together": {("nat_policy", "dynamic_group")},
            },
        ),
        migrations.CreateModel(
            name="NATPolicyDeviceM2M",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("weight", models.PositiveSmallIntegerField(default=100)),
                ("device", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="dcim.device")),
                (
                    "nat_policy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="nautobot_firewall_models.natpolicy"
                    ),
                ),
            ],
            options={
                "ordering": ["weight"],
                "unique_together": {("nat_policy", "device")},
            },
        ),
        migrations.AddField(
            model_name="natpolicy",
            name="assigned_devices",
            field=models.ManyToManyField(
                related_name="nat_policies", through="nautobot_firewall_models.NATPolicyDeviceM2M", to="dcim.Device"
            ),
        ),
        migrations.AddField(
            model_name="natpolicy",
            name="assigned_dynamic_groups",
            field=models.ManyToManyField(
                related_name="nat_policies",
                through="nautobot_firewall_models.NATPolicyDynamicGroupM2M",
                to="extras.DynamicGroup",
            ),
        ),
        migrations.AddField(
            model_name="natpolicy",
            name="nat_policy_rules",
            field=models.ManyToManyField(
                related_name="nat_policies",
                through="nautobot_firewall_models.NATPolicyRuleM2M",
                to="nautobot_firewall_models.NATPolicyRule",
            ),
        ),
        migrations.AddField(
            model_name="natpolicy",
            name="status",
            field=nautobot.extras.models.statuses.StatusField(
                default=nautobot_firewall_models.utils.get_default_status,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="nautobot_firewall_models_natpolicy_related",
                to="extras.status",
            ),
        ),
        migrations.AddField(
            model_name="natpolicy",
            name="tags",
            field=taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag"),
        ),
        migrations.AddField(
            model_name="natpolicy",
            name="tenant",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="nat_policies",
                to="tenancy.tenant",
            ),
        ),
        migrations.AddField(
            model_name="natorigsrcsvcm2m",
            name="nat_pol_rule",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="nautobot_firewall_models.natpolicyrule"
            ),
        ),
        migrations.AddField(
            model_name="natorigsrcsvcm2m",
            name="svc",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="nautobot_firewall_models.serviceobject"
            ),
        ),
        migrations.AddField(
            model_name="natorigsrcsvcgroupm2m",
            name="nat_pol_rule",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="nautobot_firewall_models.natpolicyrule"
            ),
        ),
        migrations.AddField(
            model_name="natorigsrcsvcgroupm2m",
            name="svc_group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="nautobot_firewall_models.serviceobjectgroup"
            ),
        ),
        migrations.AddField(
            model_name="natorigsrcaddrm2m",
            name="nat_pol_rule",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="nautobot_firewall_models.natpolicyrule"
            ),
        ),
        migrations.AddField(
            model_name="natorigsrcaddrgroupm2m",
            name="nat_pol_rule",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="nautobot_firewall_models.natpolicyrule"
            ),
        ),
        migrations.AddField(
            model_name="natorigdestsvcm2m",
            name="nat_pol_rule",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="nautobot_firewall_models.natpolicyrule"
            ),
        ),
        migrations.AddField(
            model_name="natorigdestsvcm2m",
            name="svc",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="nautobot_firewall_models.serviceobject"
            ),
        ),
        migrations.AddField(
            model_name="natorigdestsvcgroupm2m",
            name="nat_pol_rule",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="nautobot_firewall_models.natpolicyrule"
            ),
        ),
        migrations.AddField(
            model_name="natorigdestsvcgroupm2m",
            name="svc_group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="nautobot_firewall_models.serviceobjectgroup"
            ),
        ),
        migrations.AddField(
            model_name="natorigdestaddrm2m",
            name="nat_pol_rule",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="nautobot_firewall_models.natpolicyrule"
            ),
        ),
        migrations.AddField(
            model_name="natorigdestaddrm2m",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="nautobot_firewall_models.addressobject"
            ),
        ),
        migrations.AddField(
            model_name="natorigdestaddrgroupm2m",
            name="nat_pol_rule",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="nautobot_firewall_models.natpolicyrule"
            ),
        ),
    ]