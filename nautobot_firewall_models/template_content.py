"""Extensions of baseline Nautobot views."""

from nautobot.extras.plugins import PluginTemplateExtension

from nautobot_firewall_models.models import Policy


class DevicePolicies(PluginTemplateExtension):  # pylint: disable=abstract-method
    """Add Policy to the right side of the Device page."""

    model = "dcim.device"

    def right_page(self):
        """Add content to the right side of the Devices detail view."""
        policies = Policy.objects.filter(devices=self.context["object"])
        return self.render(
            "nautobot_firewall_models/inc/device_policies.html",
            extra_context={"policies": policies},
        )


template_extensions = [DevicePolicies]
