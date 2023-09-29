"""Custom migration for moving index to the PolicyRule."""
from django.db import migrations
from django.db.models import Count


def move_index(apps, schema_editor):
    """Custom migration for moving index to the PolicyRule."""
    # Get models to work with
    PolicyRuleM2M = apps.get_model("nautobot_firewall_models.PolicyRuleM2M")
    PolicyRule = apps.get_model("nautobot_firewall_models.PolicyRule")
    # Get list of duplicates
    duplicates = PolicyRuleM2M.objects.values("rule").annotate(Count("id")).filter(id__count__gt=1)
    duplicates = [i["rule"] for i in duplicates]
    # Create Rules for Duplicates
    for rule in PolicyRuleM2M.objects.filter(rule__in=duplicates):
        source_users = rule.rule.source_users.all()
        source_user_groups = rule.rule.source_user_groups.all()
        source_addresses = rule.rule.source_addresses.all()
        source_address_groups = rule.rule.source_address_groups.all()
        destination_addresses = rule.rule.destination_addresses.all()
        destination_address_groups = rule.rule.destination_address_groups.all()
        destination_services = rule.rule.destination_services.all()
        destination_service_groups = rule.rule.destination_service_groups.all()
        temp_rule = rule.rule
        temp_rule.id = None
        temp_rule.name = f"{rule.rule.name} for {rule.policy.name}"
        temp_rule.index = rule.index
        temp_rule.save()
        temp_rule.source_users.set(source_users)
        temp_rule.source_user_groups.set(source_user_groups)
        temp_rule.source_addresses.set(source_addresses)
        temp_rule.source_address_groups.set(source_address_groups)
        temp_rule.destination_addresses.set(destination_addresses)
        temp_rule.destination_address_groups.set(destination_address_groups)
        temp_rule.destination_services.set(destination_services)
        temp_rule.destination_service_groups.set(destination_service_groups)
        rule.rule = temp_rule
        rule.save()
    # Move Indexes for non-duplicates
    for rule in PolicyRuleM2M.objects.exclude(rule__in=duplicates):
        rule.rule.index = rule.index
        rule.rule.save()
    # Remove the duplicates
    PolicyRule.objects.filter(id__in=duplicates).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("nautobot_firewall_models", "0006_renaming_part1"),
    ]

    operations = [
        # TODO Provide Code to Reverse the move_index function
        migrations.RunPython(code=move_index, reverse_code=migrations.RunPython.noop),
    ]
