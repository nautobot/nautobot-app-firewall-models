"""Menu items."""

from nautobot.core.apps import NavMenuAddButton, NavMenuGroup, NavMenuItem, NavMenuTab

menu_items = (
    NavMenuTab(
        name="Security",
        # weight=150,
        groups=[
            NavMenuGroup(
                name="Address",
                weight=100,
                items=[
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:fqdn_list",
                        name="FQDNs",
                        permissions=["nautobot_firewall_models.view_fqdn"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_firewall_models:fqdn_add",
                                permissions=["nautobot_firewall_models.add_fqdn"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:iprange_list",
                        name="IP Ranges",
                        permissions=["nautobot_firewall_models.view_iprange"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_firewall_models:iprange_add",
                                permissions=["nautobot_firewall_models.add_iprange"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:addressobject_list",
                        name="Address Objects",
                        permissions=["nautobot_firewall_models.view_addressobject"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_firewall_models:addressobject_add",
                                permissions=["nautobot_firewall_models.add_addressobject"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:addressobjectgroup_list",
                        name="Address Object Groups",
                        permissions=["nautobot_firewall_models.view_addressobjectgroup"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_firewall_models:addressobjectgroup_add",
                                permissions=["nautobot_firewall_models.add_addressobjectgroup"],
                            ),
                        ],
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
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_firewall_models:applicationobject_add",
                                permissions=["nautobot_firewall_models.add_applicationobject"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:applicationobjectgroup_list",
                        name="Application Groups",
                        permissions=["nautobot_firewall_models.view_applicationobjectgroup"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_firewall_models:applicationobjectgroup_add",
                                permissions=["nautobot_firewall_models.add_applicationobjectgroup"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:serviceobject_list",
                        name="Service Objects",
                        permissions=["nautobot_firewall_models.view_serviceobject"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_firewall_models:serviceobject_add",
                                permissions=["nautobot_firewall_models.add_serviceobject"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:serviceobjectgroup_list",
                        name="Service Object Groups",
                        permissions=["nautobot_firewall_models.view_serviceobjectgroup"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_firewall_models:serviceobjectgroup_add",
                                permissions=["nautobot_firewall_models.add_serviceobjectgroup"],
                            ),
                        ],
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
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_firewall_models:userobject_add",
                                permissions=["nautobot_firewall_models.add_userobject"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:userobjectgroup_list",
                        name="User Object Groups",
                        permissions=["nautobot_firewall_models.view_userobjectgroup"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_firewall_models:userobjectgroup_add",
                                permissions=["nautobot_firewall_models.add_userobjectgroup"],
                            ),
                        ],
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
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_firewall_models:zone_add",
                                permissions=["nautobot_firewall_models.add_zone"],
                            ),
                        ],
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
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_firewall_models:policyrule_add",
                                permissions=["nautobot_firewall_models.add_policyrule"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:policy_list",
                        name="Policies",
                        permissions=["nautobot_firewall_models.view_policy"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_firewall_models:policy_add",
                                permissions=["nautobot_firewall_models.add_policy"],
                            ),
                        ],
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
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_firewall_models:natpolicyrule_add",
                                permissions=["nautobot_firewall_models.add_natpolicyrule"],
                            ),
                        ],
                    ),
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:natpolicy_list",
                        name="NAT Policies",
                        permissions=["nautobot_firewall_models.view_natpolicy"],
                        buttons=[
                            NavMenuAddButton(
                                link="plugins:nautobot_firewall_models:natpolicy_add",
                                permissions=["nautobot_firewall_models.add_natpolicy"],
                            ),
                        ],
                    ),
                ],
            ),
            NavMenuGroup(
                name="Aerleon",
                weight=200,
                items=[
                    NavMenuItem(
                        link="plugins:nautobot_firewall_models:aerleonpolicy_list",
                        name="Aerleon Policy Rules",
                        permissions=["nautobot_firewall_models.view_aerleonpolicy"],
                    ),
                ],
            ),
        ],
    ),
)
