"""Adds plugin items to homepage."""
from nautobot.core.apps import HomePageItem, HomePagePanel

from nautobot_firewall_models.models import Policy, PolicyRule, CapircaPolicy


layout = (
    HomePagePanel(
        weight=150,
        name="Security",
        items=(
            HomePageItem(
                name="Policies",
                model=Policy,
                weight=100,
                link="plugins:nautobot_firewall_models:policy_list",
                description="Firewall Policies",
                permissions=["nautobot_firewall_models.view_policy"],
            ),
            HomePageItem(
                name="Capirca Policies",
                model=CapircaPolicy,
                weight=150,
                link="plugins:nautobot_firewall_models:capircapolicy_list",
                description="Firewall Policies",
                permissions=["nautobot_firewall_models.view_capircapolicy"],
            ),
            HomePageItem(
                name="Policy Rules",
                model=PolicyRule,
                weight=200,
                link="plugins:nautobot_firewall_models:policyrule_list",
                description="Firewall Policies",
                permissions=["nautobot_firewall_models.view_policyrule"],
            ),
        ),
    ),
)
