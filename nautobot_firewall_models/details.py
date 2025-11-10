"""Object Detail components for golden config."""

from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.db import models
from django.urls import reverse
from nautobot.apps import ui
from nautobot.core.templatetags import helpers

from nautobot_firewall_models import tables
from nautobot_firewall_models.templatetags.fw_tags import render_truncate


class BaseFieldsPanelMixin:
    """Mixin to render a <ul> HTML list of a given url with hyperlinks, or a placeholder if none exist based on the key `key_and_reverse_url_string`."""

    def render_value(self, key, value, instance):
        """Renders a <ul> HTML list of a given url with hyperlinks, or a placeholder if none exist."""

        def _is_empty_field(val):
            if val is None:
                return True
            if isinstance(val, str) and val.strip() == "":
                return True
            try:
                if hasattr(val, "exists") and callable(val.exists):
                    return not val.exists()
            except (ObjectDoesNotExist, FieldError, TypeError, AttributeError):
                return False
            if hasattr(val, "__len__") and len(val) == 0:
                return True
            return False

        if self.key_and_reverse_url_string.get(key):
            # Defer callable check until after empty check (to catch empty ManyRelatedManager before .value())
            if _is_empty_field(value):
                return helpers.placeholder(None)

            # Now it's safe to call, and intended for dynamic/resolved values
            if callable(value) and not isinstance(value, models.Manager):
                value = value()
            full_listing_link = reverse(self.key_and_reverse_url_string[key])

            return helpers.render_m2m(
                value.all(),
                full_listing_link=full_listing_link,
                verbose_name_plural=key,
            )
        return super().render_value(key, value, instance)


class ServiceObjectGroupFieldsPanel(BaseFieldsPanelMixin, ui.ObjectFieldsPanel):
    """Set `key_and_reverse_url_string` for ServiceObjectGroup."""

    key_and_reverse_url_string = {"service_objects": "plugins:nautobot_firewall_models:serviceobject_list"}


class FQDNFieldsPanel(BaseFieldsPanelMixin, ui.ObjectFieldsPanel):
    """Set `key_and_reverse_url_string` for FQDN."""

    key_and_reverse_url_string = {"ip_addresses": "ipam:ipaddress_list"}


class NATPolicyFieldsPanel(BaseFieldsPanelMixin, ui.ObjectFieldsPanel):
    """Set `key_and_reverse_url_string` for NATPolicy."""

    key_and_reverse_url_string = {
        "assigned_devices__all": "dcim:device_list",
        "assigned_dynamic_groups__all": "extras:dynamicgroup_list",
    }


class NATPolicyRuleFieldsPanel(BaseFieldsPanelMixin, ui.ObjectFieldsPanel):
    """Set `key_and_reverse_url_string` for NATPolicyRule."""

    key_and_reverse_url_string = {"nat_policies__all": "plugins:nautobot_firewall_models:natpolicyrule_list"}


class PolicyFieldsPanel(BaseFieldsPanelMixin, ui.ObjectFieldsPanel):
    """Set `key_and_reverse_url_string` for Policy."""

    key_and_reverse_url_string = {
        "assigned_devices__all": "dcim:device_list",
        "assigned_dynamic_groups__all": "extras:dynamicgroup_list",
    }


class PolicyRuleFieldsPanel(BaseFieldsPanelMixin, ui.ObjectFieldsPanel):
    """Set `key_and_reverse_url_string` for PolicyRule."""

    key_and_reverse_url_string = {"policies__all": "plugins:nautobot_firewall_models:policyrule_list"}


class UserObjectGroupFieldsPanel(BaseFieldsPanelMixin, ui.ObjectFieldsPanel):
    """Set `key_and_reverse_url_string` for UserObjectGroup."""

    key_and_reverse_url_string = {"user_objects": "plugins:nautobot_firewall_models:userobject_list"}


class ZoneFieldsPanel(BaseFieldsPanelMixin, ui.ObjectFieldsPanel):
    """Set `key_and_reverse_url_string` for Zone."""

    key_and_reverse_url_string = {"vrfs": "ipam:vrf_list", "interfaces": "dcim:interface_list"}


address_object = ui.ObjectDetailContent(
    panels=(
        ui.ObjectFieldsPanel(
            section=ui.SectionChoices.LEFT_HALF,
            weight=100,
            fields="__all__",
        ),
    ),
)

address_object_group = ui.ObjectDetailContent(
    panels=(
        ui.ObjectFieldsPanel(
            section=ui.SectionChoices.LEFT_HALF,
            weight=100,
            # Replace with `__all__` once order is fixed
            fields=["name", "description", "status"],
        ),
        ui.ObjectsTablePanel(
            weight=100,
            section=ui.SectionChoices.FULL_WIDTH,
            table_class=tables.AddressObjectTable,
            table_filter="address_object_groups",
            related_field_name="address_object_groups",
            add_button_route=None,
        ),
    ),
)

application_object = ui.ObjectDetailContent(
    panels=(
        ui.ObjectFieldsPanel(
            section=ui.SectionChoices.LEFT_HALF,
            weight=100,
            # Replace with `__all__` once order is fixed
            fields=[
                "name",
                "description",
                "category",
                "subcategory",
                "technology",
                "risk",
                "default_ip_protocol",
                "default_type",
            ],
        ),
    ),
)


application_object_group = ui.ObjectDetailContent(
    panels=(
        ui.ObjectFieldsPanel(
            section=ui.SectionChoices.LEFT_HALF,
            weight=100,
            # Replace with `__all__` once order is fixed
            fields=["name", "description", "status"],
        ),
        ui.ObjectsTablePanel(
            weight=100,
            section=ui.SectionChoices.FULL_WIDTH,
            table_class=tables.ApplicationObjectTable,
            table_filter="application_object_groups",
            related_field_name="application_objects",
            add_button_route=None,
        ),
    ),
)

capirca_policy = ui.ObjectDetailContent(
    panels=(
        ui.ObjectFieldsPanel(
            section=ui.SectionChoices.LEFT_HALF,
            weight=100,
            fields="__all__",
            value_transforms={
                "pol": [render_truncate, helpers.pre_tag],
                "net": [render_truncate, helpers.pre_tag],
                "svc": [render_truncate, helpers.pre_tag],
                "cfg": [render_truncate, helpers.pre_tag],
            },
        ),
    ),
    extra_tabs=(
        ui.DistinctViewTab(
            weight=ui.Tab.WEIGHT_CHANGELOG_TAB + 200,
            tab_id="devicedetail",
            label="Config Details",
            url_name="plugins:nautobot_firewall_models:capircapolicy_devicedetail",
            panels=(
                ui.ObjectFieldsPanel(
                    section=ui.SectionChoices.FULL_WIDTH,
                    weight=100,
                    fields=["pol", "net", "svc", "cfg"],
                    value_transforms={
                        "pol": [helpers.pre_tag],
                        "net": [helpers.pre_tag],
                        "svc": [helpers.pre_tag],
                        "cfg": [helpers.pre_tag],
                    },
                ),
            ),
        ),
    ),
)

fqdn = ui.ObjectDetailContent(
    panels=(
        FQDNFieldsPanel(
            section=ui.SectionChoices.LEFT_HALF,
            weight=100,
            # Replace with `__all__` once order is fixed, needs additional_fields=["ip_addresses"]
            fields=["name", "description", "ip_addresses", "status"],
        ),
    ),
)


ip_range = ui.ObjectDetailContent(
    panels=(
        ui.ObjectFieldsPanel(
            section=ui.SectionChoices.LEFT_HALF,
            weight=100,
            # Replace with `__all__` once order is fixed
            fields=["description", "start_address", "end_address", "vrf", "status"],
        ),
    ),
)

nat_policy = ui.ObjectDetailContent(
    panels=(
        NATPolicyFieldsPanel(
            section=ui.SectionChoices.LEFT_HALF,
            weight=100,
            # Replace with `__all__` once order is fixed, needs additional_fields=["assigned_devices__all", "assigned_dynamic_groups__all"]
            fields=["name", "description", "assigned_devices__all", "assigned_dynamic_groups__all", "tenant", "status"],
            key_transforms={"assigned_devices__all": "Devices", "assigned_dynamic_groups__all": "Dynamic Groups"},
        ),
    ),
    extra_tabs=(
        ui.Tab(
            weight=ui.Tab.WEIGHT_CHANGELOG_TAB + 200,
            tab_id="nat-policy-rules",
            label="NAT Policy Rules",
            panels=(
                ui.Panel(
                    section=ui.SectionChoices.FULL_WIDTH,
                    weight=100,
                    template_path="nautobot_firewall_models/inc/nat_policy_expanded_rules.html",
                ),
            ),
        ),
        ui.Tab(
            weight=ui.Tab.WEIGHT_CHANGELOG_TAB + 200,
            tab_id="edit-device-weight",
            label="Edit Device Weight",
            panels=(
                ui.Panel(
                    section=ui.SectionChoices.FULL_WIDTH,
                    weight=100,
                    template_path="nautobot_firewall_models/inc/nat_policy_device_weight.html",
                ),
            ),
        ),
        ui.Tab(
            weight=ui.Tab.WEIGHT_CHANGELOG_TAB + 200,
            tab_id="edit-dynamic-group-weight",
            label="Edit Dynamic Group Weight",
            panels=(
                ui.Panel(
                    section=ui.SectionChoices.FULL_WIDTH,
                    weight=100,
                    template_path="nautobot_firewall_models/inc/nat_policy_dynamic_group_weight.html",
                ),
            ),
        ),
    ),
)

nat_policy_rule = ui.ObjectDetailContent(
    panels=(
        NATPolicyRuleFieldsPanel(
            section=ui.SectionChoices.LEFT_HALF,
            weight=100,
            # Replace with `__all__` once order is fixed, needs additional_fields=["ip_addresses"]
            fields=["description", "nat_policies__all", "status"],
            key_transforms={"nat_policies__all": "Assigned Policies"},
        ),
        ui.Panel(
            section=ui.SectionChoices.FULL_WIDTH,
            weight=100,
            template_path="nautobot_firewall_models/inc/nat_policy_expanded_rules.html",
        ),
    ),
)

policy = ui.ObjectDetailContent(
    panels=(
        PolicyFieldsPanel(
            section=ui.SectionChoices.LEFT_HALF,
            weight=100,
            # Replace with `__all__` once order is fixed, needs additional_fields=["assigned_devices__all", "assigned_dynamic_groups__all"]
            fields=["name", "description", "assigned_devices__all", "assigned_dynamic_groups__all", "tenant", "status"],
            key_transforms={"assigned_devices__all": "Devices", "assigned_dynamic_groups__all": "Dynamic Groups"},
        ),
    ),
    extra_tabs=(
        ui.Tab(
            weight=ui.Tab.WEIGHT_CHANGELOG_TAB + 200,
            tab_id="policy-rules",
            label="Policy Rules",
            panels=(
                ui.Panel(
                    section=ui.SectionChoices.FULL_WIDTH,
                    weight=100,
                    template_path="nautobot_firewall_models/inc/policy_expanded_rules.html",
                ),
            ),
        ),
        ui.Tab(
            weight=ui.Tab.WEIGHT_CHANGELOG_TAB + 200,
            tab_id="edit-device-weight",
            label="Edit Device Weight",
            panels=(
                ui.Panel(
                    section=ui.SectionChoices.FULL_WIDTH,
                    weight=100,
                    template_path="nautobot_firewall_models/inc/policy_device_weight.html",
                ),
            ),
        ),
        ui.Tab(
            weight=ui.Tab.WEIGHT_CHANGELOG_TAB + 200,
            tab_id="edit-dynamic-group-weight",
            label="Edit Dynamic Group Weight",
            panels=(
                ui.Panel(
                    section=ui.SectionChoices.FULL_WIDTH,
                    weight=100,
                    template_path="nautobot_firewall_models/inc/policy_dynamic_group_weight.html",
                ),
            ),
        ),
    ),
)

policy_rule = ui.ObjectDetailContent(
    panels=(
        PolicyRuleFieldsPanel(
            section=ui.SectionChoices.LEFT_HALF,
            weight=100,
            # Replace with `__all__` once order is fixed, needs additional_fields=["ip_addresses"]
            fields=["description", "policies__all", "status"],
            key_transforms={"policies__all": "Assigned Policies"},
        ),
        ui.Panel(
            section=ui.SectionChoices.FULL_WIDTH,
            weight=100,
            template_path="nautobot_firewall_models/inc/policy_expanded_rules.html",
        ),
    ),
)

service_object = ui.ObjectDetailContent(
    panels=(
        ui.ObjectFieldsPanel(
            section=ui.SectionChoices.LEFT_HALF,
            weight=100,
            fields="__all__",
        ),
    ),
)


service_object_group = ui.ObjectDetailContent(
    panels=(
        ServiceObjectGroupFieldsPanel(
            section=ui.SectionChoices.LEFT_HALF,
            weight=100,
            # Replace with `__all__` once order is fixed
            fields=["name", "description", "service_objects", "status"],
        ),
    ),
)

user_object = ui.ObjectDetailContent(
    panels=(
        ui.ObjectFieldsPanel(
            section=ui.SectionChoices.LEFT_HALF,
            weight=100,
            fields="__all__",
        ),
    ),
)

user_object_group = ui.ObjectDetailContent(
    panels=(
        UserObjectGroupFieldsPanel(
            section=ui.SectionChoices.LEFT_HALF,
            weight=100,
            fields=["name", "description", "user_objects", "status"],
        ),
    ),
)

zone = ui.ObjectDetailContent(
    panels=(
        ZoneFieldsPanel(
            section=ui.SectionChoices.LEFT_HALF,
            weight=100,
            fields=["name", "description", "vrfs", "interfaces", "status"],
        ),
    ),
)
