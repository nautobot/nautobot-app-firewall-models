# Generated by Django 3.2.21 on 2023-09-18 20:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ipam", "0038_vlan_group_name_unique_remove_slug"),
        ("nautobot_firewall_models", "0016_nautobot_v2_migrations"),
    ]

    operations = [
        migrations.AddField(
            model_name="addressobjectgroup",
            name="new_address_objects",
            field=models.ManyToManyField(
                blank=True, related_name="new_address_object_groups", to="nautobot_firewall_models.AddressObject"
            ),
        ),
        migrations.AddField(
            model_name="fqdn",
            name="new_ip_addresses",
            field=models.ManyToManyField(blank=True, related_name="new_fqdns", to="ipam.IPAddress"),
        ),
        migrations.AddField(
            model_name="userobjectgroup",
            name="new_user_objects",
            field=models.ManyToManyField(
                blank=True, related_name="new_user_object_groups", to="nautobot_firewall_models.UserObject"
            ),
        ),
        migrations.AddField(
            model_name="zone",
            name="new_interfaces",
            field=models.ManyToManyField(blank=True, related_name="zones", to="dcim.Interface"),
        ),
        migrations.AddField(
            model_name="zone",
            name="new_vrfs",
            field=models.ManyToManyField(blank=True, related_name="zones", to="ipam.VRF"),
        ),
        migrations.AddField(
            model_name="serviceobjectgroup",
            name="new_service_objects",
            field=models.ManyToManyField(
                blank=True, related_name="new_service_object_groups", to="nautobot_firewall_models.ServiceObject"
            ),
        ),
        migrations.AddField(
            model_name="applicationobjectgroup",
            name="new_application_objects",
            field=models.ManyToManyField(
                blank=True,
                related_name="new_application_object_groups",
                to="nautobot_firewall_models.ApplicationObject",
            ),
        ),
        # start policyrule source
        migrations.AddField(
            model_name="policyrule",
            name="new_source_users",
            field=models.ManyToManyField(
                blank=True, related_name="new_policy_rules", to="nautobot_firewall_models.UserObject"
            ),
        ),
        migrations.AddField(
            model_name="policyrule",
            name="new_source_user_groups",
            field=models.ManyToManyField(
                blank=True, related_name="new_policy_rules", to="nautobot_firewall_models.UserObjectGroup"
            ),
        ),
        migrations.AddField(
            model_name="policyrule",
            name="new_source_addresses",
            field=models.ManyToManyField(
                blank=True, related_name="new_source_policy_rules", to="nautobot_firewall_models.AddressObject"
            ),
        ),
        migrations.AddField(
            model_name="policyrule",
            name="new_source_address_groups",
            field=models.ManyToManyField(
                blank=True, related_name="new_source_policy_rules", to="nautobot_firewall_models.AddressObjectGroup"
            ),
        ),
        migrations.AddField(
            model_name="policyrule",
            name="new_source_services",
            field=models.ManyToManyField(
                blank=True, related_name="new_source_policy_rules", to="nautobot_firewall_models.ServiceObject"
            ),
        ),
        migrations.AddField(
            model_name="policyrule",
            name="new_source_service_groups",
            field=models.ManyToManyField(
                blank=True, related_name="new_source_policy_rules", to="nautobot_firewall_models.ServiceObjectGroup"
            ),
        ),
        # start policyrule destination
        migrations.AddField(
            model_name="policyrule",
            name="new_destination_addresses",
            field=models.ManyToManyField(
                blank=True, related_name="new_destination_policy_rules", to="nautobot_firewall_models.AddressObject"
            ),
        ),
        migrations.AddField(
            model_name="policyrule",
            name="new_destination_address_groups",
            field=models.ManyToManyField(
                blank=True,
                related_name="new_destination_policy_rules",
                to="nautobot_firewall_models.AddressObjectGroup",
            ),
        ),
        migrations.AddField(
            model_name="policyrule",
            name="new_destination_services",
            field=models.ManyToManyField(
                blank=True, related_name="new_destination_policy_rules", to="nautobot_firewall_models.ServiceObject"
            ),
        ),
        migrations.AddField(
            model_name="policyrule",
            name="new_destination_service_groups",
            field=models.ManyToManyField(
                blank=True,
                related_name="new_destination_policy_rules",
                to="nautobot_firewall_models.ServiceObjectGroup",
            ),
        ),
        migrations.AddField(
            model_name="policyrule",
            name="new_applications",
            field=models.ManyToManyField(
                blank=True, related_name="new_policy_rules", to="nautobot_firewall_models.ApplicationObject"
            ),
        ),
        migrations.AddField(
            model_name="policyrule",
            name="new_application_groups",
            field=models.ManyToManyField(
                blank=True, related_name="new_policy_rules", to="nautobot_firewall_models.ApplicationObjectGroup"
            ),
        ),
        # policy policyrule
        migrations.AddField(
            model_name="policy",
            name="new_policy_rules",
            field=models.ManyToManyField(
                blank=True, related_name="new_policies", to="nautobot_firewall_models.PolicyRule"
            ),
        ),
        # start natpolicyrule original source
        migrations.AddField(
            model_name="natpolicyrule",
            name="new_original_source_addresses",
            field=models.ManyToManyField(
                blank=True,
                related_name="new_original_source_nat_policy_rules",
                to="nautobot_firewall_models.AddressObject",
            ),
        ),
        migrations.AddField(
            model_name="natpolicyrule",
            name="new_original_source_address_groups",
            field=models.ManyToManyField(
                blank=True,
                related_name="new_original_source_nat_policy_rules",
                to="nautobot_firewall_models.AddressObjectGroup",
            ),
        ),
        migrations.AddField(
            model_name="natpolicyrule",
            name="new_original_source_services",
            field=models.ManyToManyField(
                blank=True,
                related_name="new_original_source_nat_policy_rules",
                to="nautobot_firewall_models.ServiceObject",
            ),
        ),
        migrations.AddField(
            model_name="natpolicyrule",
            name="new_original_source_service_groups",
            field=models.ManyToManyField(
                blank=True,
                related_name="new_original_source_nat_policy_rules",
                to="nautobot_firewall_models.ServiceObjectGroup",
            ),
        ),
        # start natpolicyrule original destination
        migrations.AddField(
            model_name="natpolicyrule",
            name="new_original_destination_addresses",
            field=models.ManyToManyField(
                blank=True,
                related_name="new_original_destination_nat_policy_rules",
                to="nautobot_firewall_models.AddressObject",
            ),
        ),
        migrations.AddField(
            model_name="natpolicyrule",
            name="new_original_destination_address_groups",
            field=models.ManyToManyField(
                blank=True,
                related_name="new_original_destination_nat_policy_rules",
                to="nautobot_firewall_models.AddressObjectGroup",
            ),
        ),
        migrations.AddField(
            model_name="natpolicyrule",
            name="new_original_destination_services",
            field=models.ManyToManyField(
                blank=True,
                related_name="new_original_destination_nat_policy_rules",
                to="nautobot_firewall_models.ServiceObject",
            ),
        ),
        migrations.AddField(
            model_name="natpolicyrule",
            name="new_original_destination_service_groups",
            field=models.ManyToManyField(
                blank=True,
                related_name="new_original_destination_nat_policy_rules",
                to="nautobot_firewall_models.ServiceObjectGroup",
            ),
        ),
        # start natpolicyrule translated source
        migrations.AddField(
            model_name="natpolicyrule",
            name="new_translated_source_addresses",
            field=models.ManyToManyField(
                blank=True,
                related_name="new_translated_source_nat_policy_rules",
                to="nautobot_firewall_models.AddressObject",
            ),
        ),
        migrations.AddField(
            model_name="natpolicyrule",
            name="new_translated_source_address_groups",
            field=models.ManyToManyField(
                blank=True,
                related_name="new_translated_source_nat_policy_rules",
                to="nautobot_firewall_models.AddressObjectGroup",
            ),
        ),
        migrations.AddField(
            model_name="natpolicyrule",
            name="new_translated_source_services",
            field=models.ManyToManyField(
                blank=True,
                related_name="new_translated_source_nat_policy_rules",
                to="nautobot_firewall_models.ServiceObject",
            ),
        ),
        migrations.AddField(
            model_name="natpolicyrule",
            name="new_translated_source_service_groups",
            field=models.ManyToManyField(
                blank=True,
                related_name="new_translated_source_nat_policy_rules",
                to="nautobot_firewall_models.ServiceObjectGroup",
            ),
        ),
        # start natpolicyrule translated destination
        migrations.AddField(
            model_name="natpolicyrule",
            name="new_translated_destination_addresses",
            field=models.ManyToManyField(
                blank=True,
                related_name="new_translated_destination_nat_policy_rules",
                to="nautobot_firewall_models.AddressObject",
            ),
        ),
        migrations.AddField(
            model_name="natpolicyrule",
            name="new_translated_destination_address_groups",
            field=models.ManyToManyField(
                blank=True,
                related_name="new_translated_destination_nat_policy_rules",
                to="nautobot_firewall_models.AddressObjectGroup",
            ),
        ),
        migrations.AddField(
            model_name="natpolicyrule",
            name="new_translated_destination_services",
            field=models.ManyToManyField(
                blank=True,
                related_name="new_translated_destination_nat_policy_rules",
                to="nautobot_firewall_models.ServiceObject",
            ),
        ),
        migrations.AddField(
            model_name="natpolicyrule",
            name="new_translated_destination_service_groups",
            field=models.ManyToManyField(
                blank=True,
                related_name="new_translated_destination_nat_policy_rules",
                to="nautobot_firewall_models.ServiceObjectGroup",
            ),
        ),
        migrations.AddField(
            model_name="natpolicy",
            name="new_nat_policy_rules",
            field=models.ManyToManyField(
                blank=True,
                related_name="new_nat_policies",
                to="nautobot_firewall_models.NATPolicyRule",
            ),
        ),
    ]
