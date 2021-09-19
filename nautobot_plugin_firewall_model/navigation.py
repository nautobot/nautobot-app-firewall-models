"""Menu items."""

from nautobot.extras.plugins import PluginMenuButton, PluginMenuItem
from nautobot.utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link="plugins:nautobot_plugin_firewall_model:fqdn_list",
        link_text="FQDNs",
        buttons=(
            PluginMenuButton(
                link="plugins:nautobot_plugin_firewall_model:fqdn_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["nautobot_plugin_firewall_model.add_fqdn"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:nautobot_plugin_firewall_model:iprange_list",
        link_text="IP Ranges",
        buttons=(
            PluginMenuButton(
                link="plugins:nautobot_plugin_firewall_model:iprange_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["nautobot_plugin_firewall_model.add_iprange"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:nautobot_plugin_firewall_model:addressgroup_list",
        link_text="Address Groups",
        buttons=(
            PluginMenuButton(
                link="plugins:nautobot_plugin_firewall_model:addressgroup_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["nautobot_plugin_firewall_model.add_addressgroup"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:nautobot_plugin_firewall_model:protocol_list",
        link_text="Protocols",
        buttons=(
            PluginMenuButton(
                link="plugins:nautobot_plugin_firewall_model:protocol_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["nautobot_plugin_firewall_model.add_protocol"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:nautobot_plugin_firewall_model:servicegroup_list",
        link_text="Service Groups",
        buttons=(
            PluginMenuButton(
                link="plugins:nautobot_plugin_firewall_model:servicegroup_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["nautobot_plugin_firewall_model.add_servicegroup"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:nautobot_plugin_firewall_model:user_list",
        link_text="Users",
        buttons=(
            PluginMenuButton(
                link="plugins:nautobot_plugin_firewall_model:user_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["nautobot_plugin_firewall_model.add_user"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:nautobot_plugin_firewall_model:usergroup_list",
        link_text="User Groups",
        buttons=(
            PluginMenuButton(
                link="plugins:nautobot_plugin_firewall_model:usergroup_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["nautobot_plugin_firewall_model.add_usergroup"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:nautobot_plugin_firewall_model:zone_list",
        link_text="Zones",
        buttons=(
            PluginMenuButton(
                link="plugins:nautobot_plugin_firewall_model:zone_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["nautobot_plugin_firewall_model.add_zone"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:nautobot_plugin_firewall_model:sourcedestination_list",
        link_text="Sources/Destinations",
        buttons=(
            PluginMenuButton(
                link="plugins:nautobot_plugin_firewall_model:sourcedestination_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["nautobot_plugin_firewall_model.add_sourcedestination"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:nautobot_plugin_firewall_model:term_list",
        link_text="Terms",
        buttons=(
            PluginMenuButton(
                link="plugins:nautobot_plugin_firewall_model:term_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["nautobot_plugin_firewall_model.add_term"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:nautobot_plugin_firewall_model:policy_list",
        link_text="Policies",
        buttons=(
            PluginMenuButton(
                link="plugins:nautobot_plugin_firewall_model:policy_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["nautobot_plugin_firewall_model.add_policy"],
            ),
        ),
    ),
)
