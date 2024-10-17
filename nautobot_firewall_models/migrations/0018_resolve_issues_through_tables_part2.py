# Generated by Django 3.2.21 on 2023-09-18 20:29

from django.db import migrations

affected_models = [
    {"model": "nautobot_firewall_models.AddressObjectGroup", "old": "address_objects", "new": "new_address_objects"},
    {"model": "nautobot_firewall_models.FQDN", "old": "ip_addresses", "new": "new_ip_addresses"},
    {"model": "nautobot_firewall_models.Zone", "old": "interfaces", "new": "new_interfaces"},
    {"model": "nautobot_firewall_models.Zone", "old": "vrfs", "new": "new_vrfs"},
    {"model": "nautobot_firewall_models.ServiceObjectGroup", "old": "service_objects", "new": "new_service_objects"},
    {
        "model": "nautobot_firewall_models.ApplicationObjectGroup",
        "old": "application_objects",
        "new": "new_application_objects",
    },
    # policy rule source
    {"model": "nautobot_firewall_models.PolicyRule", "old": "source_users", "new": "new_source_users"},
    {"model": "nautobot_firewall_models.PolicyRule", "old": "source_user_groups", "new": "new_source_user_groups"},
    {"model": "nautobot_firewall_models.PolicyRule", "old": "source_addresses", "new": "new_source_addresses"},
    {
        "model": "nautobot_firewall_models.PolicyRule",
        "old": "source_address_groups",
        "new": "new_source_address_groups",
    },
    {"model": "nautobot_firewall_models.PolicyRule", "old": "source_services", "new": "new_source_services"},
    {
        "model": "nautobot_firewall_models.PolicyRule",
        "old": "source_service_groups",
        "new": "new_source_service_groups",
    },
    # policy rule dest
    {
        "model": "nautobot_firewall_models.PolicyRule",
        "old": "destination_addresses",
        "new": "new_destination_addresses",
    },
    {
        "model": "nautobot_firewall_models.PolicyRule",
        "old": "destination_address_groups",
        "new": "new_destination_address_groups",
    },
    {"model": "nautobot_firewall_models.PolicyRule", "old": "destination_services", "new": "new_destination_services"},
    {
        "model": "nautobot_firewall_models.PolicyRule",
        "old": "destination_service_groups",
        "new": "new_destination_service_groups",
    },
    {"model": "nautobot_firewall_models.PolicyRule", "old": "applications", "new": "new_applications"},
    {"model": "nautobot_firewall_models.PolicyRule", "old": "application_groups", "new": "new_application_groups"},
    # policy policyrule
    {"model": "nautobot_firewall_models.Policy", "old": "policy_rules", "new": "new_policy_rules"},
    # natpolicyrule original
    {
        "model": "nautobot_firewall_models.NATPolicyRule",
        "old": "original_source_addresses",
        "new": "new_original_source_addresses",
    },
    {
        "model": "nautobot_firewall_models.NATPolicyRule",
        "old": "original_source_address_groups",
        "new": "new_original_source_address_groups",
    },
    {
        "model": "nautobot_firewall_models.NATPolicyRule",
        "old": "original_source_services",
        "new": "new_original_source_services",
    },
    {
        "model": "nautobot_firewall_models.NATPolicyRule",
        "old": "original_source_service_groups",
        "new": "new_original_source_service_groups",
    },
    {
        "model": "nautobot_firewall_models.NATPolicyRule",
        "old": "original_destination_addresses",
        "new": "new_original_destination_addresses",
    },
    {
        "model": "nautobot_firewall_models.NATPolicyRule",
        "old": "original_destination_address_groups",
        "new": "new_original_destination_address_groups",
    },
    {
        "model": "nautobot_firewall_models.NATPolicyRule",
        "old": "original_destination_services",
        "new": "new_original_destination_services",
    },
    {
        "model": "nautobot_firewall_models.NATPolicyRule",
        "old": "original_destination_service_groups",
        "new": "new_original_destination_service_groups",
    },
    # natpolicyrule translated
    {
        "model": "nautobot_firewall_models.NATPolicyRule",
        "old": "translated_source_addresses",
        "new": "new_translated_source_addresses",
    },
    {
        "model": "nautobot_firewall_models.NATPolicyRule",
        "old": "translated_source_address_groups",
        "new": "new_translated_source_address_groups",
    },
    {
        "model": "nautobot_firewall_models.NATPolicyRule",
        "old": "translated_source_services",
        "new": "new_translated_source_services",
    },
    {
        "model": "nautobot_firewall_models.NATPolicyRule",
        "old": "translated_source_service_groups",
        "new": "new_translated_source_service_groups",
    },
    {
        "model": "nautobot_firewall_models.NATPolicyRule",
        "old": "translated_destination_addresses",
        "new": "new_translated_destination_addresses",
    },
    {
        "model": "nautobot_firewall_models.NATPolicyRule",
        "old": "translated_destination_address_groups",
        "new": "new_translated_destination_address_groups",
    },
    {
        "model": "nautobot_firewall_models.NATPolicyRule",
        "old": "translated_destination_services",
        "new": "new_translated_destination_services",
    },
    {
        "model": "nautobot_firewall_models.NATPolicyRule",
        "old": "translated_destination_service_groups",
        "new": "new_translated_destination_service_groups",
    },
    {
        "model": "nautobot_firewall_models.NATPolicy",
        "old": "nat_policy_rules",
        "new": "new_nat_policy_rules",
    },
]


def migrate_m2m(apps, schema_editor, new="new", old="old"):
    for fields in affected_models:
        model_class = apps.get_model(fields["model"])
        for instance in model_class.objects.all():
            new_field = getattr(instance, fields[new])
            old_field = getattr(instance, fields[old])
            new_field.set(old_field.all())


def reverse_migrate_m2m(apps, schema_editor):
    migrate_m2m(apps=apps, schema_editor=schema_editor, new="old", old="new")


class Migration(migrations.Migration):
    dependencies = [
        ("ipam", "0038_vlan_group_name_unique_remove_slug"),
        ("nautobot_firewall_models", "0017_resolve_issues_through_tables_part1"),
    ]

    operations = [
        migrations.RunPython(code=migrate_m2m, reverse_code=reverse_migrate_m2m),
    ]