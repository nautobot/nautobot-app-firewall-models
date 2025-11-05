"""Menu items."""

from nautobot.apps.ui import (
    NavigationIconChoices,
    NavigationWeightChoices,
    NavMenuGroup,
    NavMenuItem,
    NavMenuTab,
)

menu_items = (
    NavMenuTab(
        name="Security",
        icon=NavigationIconChoices.SECURITY,
        weight=NavigationWeightChoices.SECURITY,
        groups=[
            NavMenuGroup(
                name="Address",
                weight=100,
                items=[
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:fqdn_list",
                        name="FQDNs",
                        permissions=["nautobot_firewall_models.view_fqdn"],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:iprange_list",
                        name="IP Ranges",
                        permissions=["nautobot_firewall_models.view_iprange"],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:addressobject_list",
                        name="Address Objects",
                        permissions=["nautobot_firewall_models.view_addressobject"],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:addressobjectgroup_list",
                        name="Address Object Groups",
                        permissions=["nautobot_firewall_models.view_addressobjectgroup"],
                    ),
                ],
            ),
            NavMenuGroup(
                name="Service",
                weight=200,
                items=[
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:applicationobject_list",
                        name="Applications",
                        permissions=["nautobot_firewall_models.view_applicationobject"],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:applicationobjectgroup_list",
                        name="Application Groups",
                        permissions=["nautobot_firewall_models.view_applicationobjectgroup"],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:serviceobject_list",
                        name="Service Objects",
                        permissions=["nautobot_firewall_models.view_serviceobject"],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:serviceobjectgroup_list",
                        name="Service Object Groups",
                        permissions=["nautobot_firewall_models.view_serviceobjectgroup"],
                    ),
                ],
            ),
            NavMenuGroup(
                name="User",
                weight=200,
                items=[
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:userobject_list",
                        name="User Objects",
                        permissions=["nautobot_firewall_models.view_userobject"],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:userobjectgroup_list",
                        name="User Object Groups",
                        permissions=["nautobot_firewall_models.view_userobjectgroup"],
                    ),
                ],
            ),
            NavMenuGroup(
                name="Zone",
                weight=200,
                items=[
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:zone_list",
                        name="Zones",
                        permissions=["nautobot_firewall_models.view_zone"],
                    ),
                ],
            ),
            NavMenuGroup(
                name="Policy",
                weight=200,
                items=[
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:policyrule_list",
                        name="Policy Rules",
                        permissions=["nautobot_firewall_models.view_policyrule"],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:policy_list",
                        name="Policies",
                        permissions=["nautobot_firewall_models.view_policy"],
                    ),
                ],
            ),
            NavMenuGroup(
                name="NAT Policy",
                weight=200,
                items=[
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:natpolicyrule_list",
                        name="NAT Policy Rules",
                        permissions=["nautobot_firewall_models.view_natpolicyrule"],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:natpolicy_list",
                        name="NAT Policies",
                        permissions=["nautobot_firewall_models.view_natpolicy"],
                    ),
                ],
            ),
            NavMenuGroup(
                name="Capirca",
                weight=200,
                items=[
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:capircapolicy_list",
                        name="Capirca Policy Rules",
                        permissions=["nautobot_firewall_models.view_capircapolicy"],
                    ),
                ],
            ),
        ],
    ),
)
