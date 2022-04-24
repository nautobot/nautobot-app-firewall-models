"""Extensions of baseline Nautobot views."""
from nautobot.extras.plugins import PluginTemplateExtension


class DevicePolicies(PluginTemplateExtension):  # pylint: disable=abstract-method
    """Add Policy to the right side of the Device page."""

    model = "dcim.device"

    def right_page(self):
        """Add content to the right side of the Devices detail view."""
        return self.render(
            "nautobot_firewall_models/inc/device_policies.html",
            extra_context={"policies": self.context["object"].policydevicem2m_set.all()},
        )


class DynamicGroupDevicePolicies(PluginTemplateExtension):  # pylint: disable=abstract-method
    """Add Policy to the right side of the Device page."""

    model = "dcim.device"

    def right_page(self):
        """Add content to the right side of the Devices detail view."""
        return self.render(
            "nautobot_firewall_models/inc/dynamic_group_device_policies.html",
            extra_context={"dynamic_groups": self.context["object"].dynamic_groups.all()},
        )


template_extensions = [DynamicGroupDevicePolicies, DevicePolicies]
