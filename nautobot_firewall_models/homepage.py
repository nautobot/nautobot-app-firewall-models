"""Adds App items to homepage."""

from nautobot.core.apps import HomePageItem, HomePagePanel

from nautobot_firewall_models.models import CapircaPolicy, FirewallConfig, NATPolicy, NATPolicyRule, Policy, PolicyRule

layout = (
    HomePagePanel(
        weight=150,
        name="Security",
        items=(
            HomePageItem(
                name="Security Policies",
                model=Policy,
                weight=100,
                link="plugins:nautobot_firewall_models:policy_list",
                description="Firewall Policies",
                permissions=["nautobot_firewall_models.view_policy"],
            ),
            HomePageItem(
                name="NAT Policies",
                model=NATPolicy,
                weight=200,
                link="plugins:nautobot_firewall_models:natpolicy_list",
                description="NAT Policies",
                permissions=["nautobot_firewall_models.view_natpolicy"],
            ),
            HomePageItem(
                name="Firewall Config",
                model=FirewallConfig,
                weight=300,
                link="plugins:nautobot_firewall_models:firewallconfig_list",
                description="Firewall Configurations",
                permissions=["nautobot_firewall_models.view_firewallconfig"],
            ),
            HomePageItem(
                name="Capirca Policies",
                model=CapircaPolicy,
                weight=300,
                link="plugins:nautobot_firewall_models:capircapolicy_list",
                description="Firewall Policies",
                permissions=["nautobot_firewall_models.view_capircapolicy"],
            ),
            HomePageItem(
                name="Security Rules",
                model=PolicyRule,
                weight=400,
                link="plugins:nautobot_firewall_models:policyrule_list",
                description="Firewall Policies",
                permissions=["nautobot_firewall_models.view_policyrule"],
            ),
            HomePageItem(
                name="NAT Rules",
                model=NATPolicyRule,
                weight=500,
                link="plugins:nautobot_firewall_models:natpolicyrule_list",
                description="NAT Policies",
                permissions=["nautobot_firewall_models.view_natpolicyrule"],
            ),
        ),
    ),
)
