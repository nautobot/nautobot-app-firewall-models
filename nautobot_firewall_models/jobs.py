"""Jobs to run backups, intended config, and compliance."""
from nautobot.extras.jobs import Job, MultiObjectVar, get_task_logger
from nautobot.core.celery import register_jobs

from nautobot.dcim.models import Device
from nautobot_firewall_models.models import CapircaPolicy
from nautobot_firewall_models.models import Policy

logger = get_task_logger(__name__)


name = "Capirca Jobs"  # pylint: disable=invalid-name


class RunCapircaJob(Job):  # pylint disable=too-few-public-method
    """Class definition to use as Mixin for form definitions."""

    device = MultiObjectVar(model=Device, required=False)

    class Meta:
        """Meta object boilerplate for reservations."""

        name = "Generate FW Config via Capirca."
        description = "Generate FW Config via Capirca and update the models."
        commit_default = True
        has_sensitive_variables = False

    def run(self, device):  # pylint: disable=arguments-differ
        """Run a job to remove legacy reservations."""
        queryset = []
        devices = []
        if device:
            queryset = device
        else:
            # TODO: see if this logic can be optimized
            for policy in Policy.objects.all():
                for dyn in policy.assigned_dynamic_groups.get_queryset():
                    if not queryset:
                        queryset = dyn.get_queryset()
                    else:
                        queryset.union(dyn.get_queryset())  # pylint: disable=no-member
                for dev in policy.assigned_devices.all():
                    devices.append(dev.pk)
        for dev in queryset:
            devices.append(dev.pk)

        devices = list(set(devices))
        for dev in devices:
            device_obj = Device.objects.get(pk=dev)
            logger.debug("Running against Device: `%s`", str(device_obj))
            CapircaPolicy.objects.update_or_create(device=device_obj)
            logger.info(f"{device_obj} Updated", extra={"object": device_obj})


jobs = [RunCapircaJob]
register_jobs(*jobs)
