# Generated by Django 3.1.13 on 2021-09-19 00:39

from django.db import migrations, models
import django.db.models.deletion
import nautobot.ipam.fields
import taggit.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("extras", "0011_fileattachment_fileproxy"),
        ("dcim", "0005_device_local_context_schema"),
        ("ipam", "0004_fixup_p2p_broadcast"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="AddressGroup",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("description", models.CharField(blank=True, max_length=200)),
                ("name", models.CharField(max_length=50, unique=True)),
            ],
            options={
                "verbose_name_plural": "Zones",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="FQDN",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("description", models.CharField(blank=True, max_length=200)),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
            options={
                "verbose_name_plural": "FQDNs",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="IPRange",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("start_address", nautobot.ipam.fields.VarbinaryIPField(db_index=True)),
                ("end_address", nautobot.ipam.fields.VarbinaryIPField(db_index=True)),
                ("description", models.CharField(blank=True, max_length=200)),
                ("size", models.PositiveIntegerField(editable=False)),
            ],
            options={
                "verbose_name_plural": "IP Ranges",
                "ordering": ["start_address"],
            },
        ),
        migrations.CreateModel(
            name="Policy",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("description", models.CharField(blank=True, max_length=200)),
                ("name", models.CharField(max_length=50, unique=True)),
            ],
            options={
                "verbose_name_plural": "Policies",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Protocol",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("description", models.CharField(blank=True, max_length=200)),
                ("name", models.CharField(max_length=50)),
                ("slug", models.SlugField(editable=False)),
                ("port", models.IntegerField()),
                ("tcp_udp", models.CharField(blank=True, max_length=3, null=True)),
            ],
            options={
                "verbose_name_plural": "Protocols",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="SourceDestination",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("description", models.CharField(blank=True, max_length=200)),
                ("assigned_address_id", models.UUIDField(blank=True, null=True)),
                ("assigned_user_id", models.UUIDField(blank=True, null=True)),
                ("assigned_service_id", models.UUIDField(blank=True, null=True)),
                (
                    "assigned_address_type",
                    models.ForeignKey(
                        blank=True,
                        limit_choices_to=models.Q(
                            models.Q(
                                models.Q(("app_label", "ipam"), ("model", "ipaddress")),
                                models.Q(("app_label", "ipam"), ("model", "prefix")),
                                models.Q(("app_label", "nautobot_plugin_firewall_model"), ("model", "iprange")),
                                models.Q(("app_label", "nautobot_plugin_firewall_model"), ("model", "addressgroup")),
                                models.Q(("app_label", "nautobot_plugin_firewall_model"), ("model", "fqdn")),
                                _connector="OR",
                            )
                        ),
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "assigned_service_type",
                    models.ForeignKey(
                        blank=True,
                        limit_choices_to=models.Q(
                            models.Q(
                                models.Q(("app_label", "nautobot_plugin_firewall_model"), ("model", "protocol")),
                                models.Q(("app_label", "nautobot_plugin_firewall_model"), ("model", "servicegroup")),
                                _connector="OR",
                            )
                        ),
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "assigned_user_type",
                    models.ForeignKey(
                        blank=True,
                        limit_choices_to=models.Q(
                            models.Q(
                                models.Q(("app_label", "nautobot_plugin_firewall_model"), ("model", "user")),
                                models.Q(("app_label", "nautobot_plugin_firewall_model"), ("model", "usergroup")),
                                _connector="OR",
                            )
                        ),
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Sources or Destinations",
                "ordering": ["description"],
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("username", models.CharField(max_length=50, unique=True)),
                ("name", models.CharField(blank=True, max_length=50)),
            ],
            options={
                "verbose_name_plural": "User",
                "ordering": ["username"],
            },
        ),
        migrations.CreateModel(
            name="Zone",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("description", models.CharField(blank=True, max_length=200)),
                ("name", models.CharField(max_length=50, unique=True)),
                ("interfaces", models.ManyToManyField(blank=True, to="dcim.Interface")),
                ("vrfs", models.ManyToManyField(blank=True, to="ipam.VRF")),
            ],
            options={
                "verbose_name_plural": "Zones",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="UserGroup",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("description", models.CharField(blank=True, max_length=200)),
                ("name", models.CharField(max_length=50, unique=True)),
                ("users", models.ManyToManyField(blank=True, to="nautobot_plugin_firewall_model.User")),
            ],
            options={
                "verbose_name_plural": "User Groups",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Term",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("index", models.IntegerField()),
                ("action", models.CharField(max_length=20)),
                ("log", models.BooleanField(default=False)),
                (
                    "destination",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="term_destination",
                        to="nautobot_plugin_firewall_model.sourcedestination",
                    ),
                ),
                (
                    "source",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="term_source",
                        to="nautobot_plugin_firewall_model.sourcedestination",
                    ),
                ),
                ("tags", taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag")),
            ],
            options={
                "verbose_name_plural": "Terms",
                "ordering": ["index"],
            },
        ),
        migrations.AddField(
            model_name="sourcedestination",
            name="zone",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="nautobot_plugin_firewall_model.zone"
            ),
        ),
        migrations.CreateModel(
            name="ServiceGroup",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                ("description", models.CharField(blank=True, max_length=200)),
                ("name", models.CharField(max_length=50, unique=True)),
                ("protocols", models.ManyToManyField(blank=True, to="nautobot_plugin_firewall_model.Protocol")),
            ],
            options={
                "verbose_name_plural": "ServiceGroups",
                "ordering": ["name"],
            },
        ),
        migrations.AddConstraint(
            model_name="protocol",
            constraint=models.UniqueConstraint(fields=("slug", "port", "tcp_udp"), name="unique_with_tcp_udp"),
        ),
        migrations.AddConstraint(
            model_name="protocol",
            constraint=models.UniqueConstraint(
                condition=models.Q(tcp_udp=None), fields=("slug", "port"), name="unique_without_tcp_udp"
            ),
        ),
        migrations.AddField(
            model_name="policy",
            name="terms",
            field=models.ManyToManyField(to="nautobot_plugin_firewall_model.Term"),
        ),
        migrations.AddField(
            model_name="iprange",
            name="vrf",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="ip_ranges",
                to="ipam.vrf",
            ),
        ),
        migrations.AddField(
            model_name="addressgroup",
            name="ip_addresses",
            field=models.ManyToManyField(blank=True, to="ipam.IPAddress"),
        ),
        migrations.AddField(
            model_name="addressgroup",
            name="ip_ranges",
            field=models.ManyToManyField(blank=True, to="nautobot_plugin_firewall_model.IPRange"),
        ),
        migrations.AddField(
            model_name="addressgroup",
            name="prefixes",
            field=models.ManyToManyField(blank=True, to="ipam.Prefix"),
        ),
        migrations.AddConstraint(
            model_name="iprange",
            constraint=models.UniqueConstraint(fields=("start_address", "end_address", "vrf"), name="unique_with_vrf"),
        ),
        migrations.AddConstraint(
            model_name="iprange",
            constraint=models.UniqueConstraint(
                condition=models.Q(vrf=None), fields=("start_address", "end_address"), name="unique_without_vrf"
            ),
        ),
    ]
