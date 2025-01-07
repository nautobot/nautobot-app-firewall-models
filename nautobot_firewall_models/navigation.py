"""Menu items."""

from nautobot.apps.ui import NavMenuAddButton, NavMenuGroup, NavMenuItem, NavMenuTab

items = (
    NavMenuItem(
        link="plugins:nautobot_firewall_models:iprange_list",
        name="Nautobot Firewall Models",
        permissions=["nautobot_firewall_models.view_iprange"],
        buttons=(
            NavMenuAddButton(
                link="plugins:nautobot_firewall_models:iprange_add",
                permissions=["nautobot_firewall_models.add_iprange"],
            ),
        ),
    ),
)

menu_items = (
    NavMenuTab(
        name="Apps",
        groups=(NavMenuGroup(name="Nautobot Firewall Models", items=tuple(items)),),
    ),
)
