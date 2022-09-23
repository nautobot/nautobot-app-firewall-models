"""Extensions of baseline Nautobot views."""
from nautobot.extras.plugins import PluginTemplateExtension
from nautobot_firewall_models.models import CapircaPolicy


class DevicePolicies(PluginTemplateExtension):  # pylint: disable=abstract-method
    """Add Policy to the right side of the Device page."""

    model = "dcim.device"

    def right_page(self):
        """Add content to the right side of the Devices detail view."""
        return self.render(
            "nautobot_firewall_models/inc/device_policies.html",
            extra_context={
                "policies": self.context["object"].policydevicem2m_set.all(),
                "nat_policies": self.context["object"].natpolicydevicem2m_set.all()
            },
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


class DynamicGroupPolicies(PluginTemplateExtension):  # pylint: disable=abstract-method
    """Add Policy to the right side of the Device page."""

    model = "extras.dynamicgroup"

    def right_page(self):
        """Add content to the right side of the Devices detail view."""
        return self.render(
            "nautobot_firewall_models/inc/dynamic_group_policies.html",
            extra_context={
                "policies": self.context["object"].policydynamicgroupm2m_set.all(),
                "nat_policies": self.context["object"].natpolicydynamicgroupm2m_set.all()
            },
        )


class CapircaPolicies(PluginTemplateExtension):  # pylint: disable=abstract-method
    """Add Policy to the right side of the Device page."""

    model = "dcim.device"

    def right_page(self):
        """Add content to the right side of the Devices detail view."""
        try:
            obj = CapircaPolicy.objects.get(device=self.context["object"])
            return self.render(
                "nautobot_firewall_models/inc/capirca_policy.html",
                extra_context={"capirca_object": obj},
            )
        except CapircaPolicy.DoesNotExist:
            return ""


template_extensions = [DynamicGroupDevicePolicies, DevicePolicies, DynamicGroupPolicies, CapircaPolicies]
