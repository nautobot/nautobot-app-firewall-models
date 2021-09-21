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
        link="plugins:nautobot_plugin_firewall_model:addressobject_list",
        link_text="Address Objects",
        buttons=(
            PluginMenuButton(
                link="plugins:nautobot_plugin_firewall_model:addressobject_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["nautobot_plugin_firewall_model.add_addressobject"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:nautobot_plugin_firewall_model:addressobjectgroup_list",
        link_text="Address Object Groups",
        buttons=(
            PluginMenuButton(
                link="plugins:nautobot_plugin_firewall_model:addressobjectgroup_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["nautobot_plugin_firewall_model.add_addressobjectgroup"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:nautobot_plugin_firewall_model:addresspolicyobject_list",
        link_text="Address Policy Objects",
        buttons=(
            PluginMenuButton(
                link="plugins:nautobot_plugin_firewall_model:addresspolicyobject_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["nautobot_plugin_firewall_model.add_addresspolicyobject"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:nautobot_plugin_firewall_model:serviceobject_list",
        link_text="Service Objects",
        buttons=(
            PluginMenuButton(
                link="plugins:nautobot_plugin_firewall_model:serviceobject_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["nautobot_plugin_firewall_model.add_serviceobject"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:nautobot_plugin_firewall_model:serviceobjectgroup_list",
        link_text="Service Object Groups",
        buttons=(
            PluginMenuButton(
                link="plugins:nautobot_plugin_firewall_model:serviceobjectgroup_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["nautobot_plugin_firewall_model.add_serviceobjectgroup"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:nautobot_plugin_firewall_model:servicepolicyobject_list",
        link_text="Service Policy Objects",
        buttons=(
            PluginMenuButton(
                link="plugins:nautobot_plugin_firewall_model:servicepolicyobject_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["nautobot_plugin_firewall_model.add_servicepolicyobject"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:nautobot_plugin_firewall_model:userobject_list",
        link_text="User Objects",
        buttons=(
            PluginMenuButton(
                link="plugins:nautobot_plugin_firewall_model:userobject_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["nautobot_plugin_firewall_model.add_userobject"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:nautobot_plugin_firewall_model:userobjectgroup_list",
        link_text="User Object Groups",
        buttons=(
            PluginMenuButton(
                link="plugins:nautobot_plugin_firewall_model:userobjectgroup_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["nautobot_plugin_firewall_model.add_usergroup"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:nautobot_plugin_firewall_model:userpolicyobject_list",
        link_text="User Policy Objects",
        buttons=(
            PluginMenuButton(
                link="plugins:nautobot_plugin_firewall_model:userpolicyobject_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["nautobot_plugin_firewall_model.add_userpolicyobject"],
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
        link="plugins:nautobot_plugin_firewall_model:source_list",
        link_text="Sources",
        buttons=(
            PluginMenuButton(
                link="plugins:nautobot_plugin_firewall_model:source_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["nautobot_plugin_firewall_model.add_source"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:nautobot_plugin_firewall_model:destination_list",
        link_text="Destinations",
        buttons=(
            PluginMenuButton(
                link="plugins:nautobot_plugin_firewall_model:destination_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["nautobot_plugin_firewall_model.add_destination"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:nautobot_plugin_firewall_model:policyrule_list",
        link_text="Policy Rules",
        buttons=(
            PluginMenuButton(
                link="plugins:nautobot_plugin_firewall_model:policyrule_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["nautobot_plugin_firewall_model.add_policyrule"],
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
