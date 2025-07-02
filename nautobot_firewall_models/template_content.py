"""Extensions of baseline Nautobot views."""

from abc import ABCMeta

from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy
from nautobot.apps.ui import TemplateExtension

from nautobot_firewall_models.models import AerleonPolicy


class DevicePolicies(TemplateExtension):  # pylint: disable=abstract-method
    """Add Policy to the right side of the Device page."""

    model = "dcim.device"

    def right_page(self):
        """Add content to the right side of the Devices detail view."""
        return self.render(
            "nautobot_firewall_models/inc/object_policies.html",
            extra_context={
                "policies": self.context["object"].policydevicem2m_set.all(),
                "nat_policies": self.context["object"].natpolicydevicem2m_set.all(),
            },
        )


class VirtualMachinePolicies(TemplateExtension):  # pylint: disable=abstract-method
    """Add Policy to the right side of the Virtual Machine page."""

    model = "virtualization.virtualmachine"

    def right_page(self):
        """Add Policy to the right side of the Virtual Machine page."""
        return self.render(
            "nautobot_firewall_models/inc/object_policies.html",
            extra_context={
                "policies": self.context["object"].policyvirtualmachinem2m_set.all(),
                "nat_policies": self.context["object"].natpolicyvirtualmachinem2m_set.all(),
            },
        )


class DynamicGroupDevicePolicies(TemplateExtension):  # pylint: disable=abstract-method
    """Add Policy to the right side of the Device page."""

    model = "dcim.device"

    def right_page(self):
        """Add content to the right side of the Devices detail view."""
        return self.render(
            "nautobot_firewall_models/inc/dynamic_group_device_policies.html",
            extra_context={"dynamic_groups": self.context["object"].dynamic_groups.all()},
        )


class DynamicGroupVirtualMachinePolicies(TemplateExtension):  # pylint: disable=abstract-method
    """Add Policy to the right side of the Virtual Machine page."""

    model = "virtualization.virtualmachine"

    def right_page(self):
        """Add content to the right side of the Devices detail view."""
        return self.render(
            "nautobot_firewall_models/inc/dynamic_group_virtual_machine_policies.html",
            extra_context={"dynamic_groups": self.context["object"].dynamic_groups.all()},
        )


class DynamicGroupPolicies(TemplateExtension):  # pylint: disable=abstract-method
    """Add Policy to the right side of the Device page."""

    model = "extras.dynamicgroup"

    def right_page(self):
        """Add content to the right side of the Devices detail view."""
        return self.render(
            "nautobot_firewall_models/inc/dynamic_group_policies.html",
            extra_context={
                "policies": self.context["object"].policydynamicgroupm2m_set.all(),
                "nat_policies": self.context["object"].natpolicydynamicgroupm2m_set.all(),
            },
        )


class AbstractAerleonPolicies(TemplateExtension, metaclass=ABCMeta):  # pylint: disable=abstract-method
    """Add Policy to the right side of the model page (has to be subclassed)."""

    def right_page(self):
        """Add content to the right side of the Devices detail view."""
        try:
            obj = self.context["object"]
            ct = ContentType.objects.get_for_model(obj)
            aerleon_object = AerleonPolicy.objects.get(content_type=ct, object_id=obj.id)

            q = ""
            if ct.app_label == "virtualization" and ct.model == "virtualmachine":
                q = f"virtual_machine={obj.id}"
            elif ct.app_label == "dcim" and ct.model == "device":
                q = f"device={obj.id}"

            return self.render(
                "nautobot_firewall_models/inc/aerleon_policy.html",
                extra_context={
                    "aerleon_object": aerleon_object,
                    "run_job_link": f'{reverse_lazy("extras:job_run_by_class_path", kwargs={"class_path": "nautobot_firewall_models.jobs.RunAerleonJob"})}?{q}',
                },
            )
        except AerleonPolicy.DoesNotExist:
            return ""


class AerleonDevicePolicies(AbstractAerleonPolicies):  # pylint: disable=abstract-method
    """Add Policy to the right side of the Device page."""

    model = "dcim.device"


class AerleonVirtualMachinePolicies(AbstractAerleonPolicies):  # pylint: disable=abstract-method
    """Add Policy to the right side of the Virtual Machine page."""

    model = "virtualization.virtualmachine"


template_extensions = [
    DynamicGroupDevicePolicies,
    DynamicGroupVirtualMachinePolicies,
    DevicePolicies,
    VirtualMachinePolicies,
    DynamicGroupPolicies,
    AerleonDevicePolicies,
    AerleonVirtualMachinePolicies,
]
