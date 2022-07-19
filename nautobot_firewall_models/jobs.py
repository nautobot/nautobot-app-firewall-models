"""Jobs to run backups, intended config, and compliance."""
import logging

from nautobot.extras.jobs import Job, MultiObjectVar

from nautobot.dcim.models import Device
from nautobot_firewall_models.models import CapircaPolicy
from nautobot_firewall_models.models.core_models import Policy

LOGGER = logging.getLogger(__name__)


name = "Capirca Jobs"  # pylint: disable=invalid-name


class RunCapircaJob(Job):  # pylint disable=too-few-public-method
    """Class definition to use as Mixin for form definitions."""

    device = MultiObjectVar(model=Device, required=False)

    class Meta:
        """Meta object boilerplate for reservations."""

        name = "Generate FW Config via Capirca."
        description = "Generate FW Config via Capirca and update the models."
        commit_default = True

    def run(self, data, commit):
        """Run a job to remove legacy reservations."""
        queryset = []
        devices = []
        if data.get("device"):
            queryset = data["device"]
        else:
            # TODO: see if this logic can be optimized
            for policy in Policy.objects.all():
                for dyn in policy.assigned_dynamic_groups.get_queryset():
                    if not queryset:
                        queryset = dyn.get_queryset()
                    else:
                        queryset.union(dyn.get_queryset())  # pylint: disable=no-member
                for device in policy.assigned_devices.all():
                    devices.append(device.pk)
        for device in queryset:
            devices.append(device.pk)

        devices = list(set(devices))
        for device in devices:
            device_obj = Device.objects.get(pk=device)
            LOGGER.debug("Running against Device: `%s`", str(device_obj))
            CapircaPolicy.objects.update_or_create(device=device_obj)
            self.log_info(obj=device_obj, message=f"{device_obj} Updated")


jobs = [RunCapircaJob]
