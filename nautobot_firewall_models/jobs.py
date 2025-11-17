"""Jobs to run backups, intended config, and compliance."""

from nautobot.core.celery import register_jobs
from nautobot.dcim.models import Device
from nautobot.extras.jobs import Job, MultiObjectVar, get_task_logger

from nautobot_firewall_models.models import CapircaPolicy, Policy
from nautobot_firewall_models.models.firewall_config import FirewallConfig

logger = get_task_logger(__name__)


name = "Capirca Jobs"  # pylint: disable=invalid-name


class RunCapircaJob(Job):  # pylint disable=too-few-public-method
    """Job that creates firewall configs from Capirca policies."""

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
            logger.info("%s Updated", device_obj, extra={"object": device_obj})


class RunFirewallConfigJob(Job):  # pylint disable=too-few-public-method
    """Job that creates firewall configs from your chosen method."""

    device = MultiObjectVar(model=Device, required=False)

    class Meta:
        """Meta object boilerplate for reservations."""

        name = "Generate FW Config."
        description = "Generate FW Config from Aerleon, Capirca, or your own custom method."
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
            FirewallConfig.objects.update_or_create(device=device_obj)
            logger.info("%s Updated", device_obj, extra={"object": device_obj})


register_jobs(RunCapircaJob)
register_jobs(RunFirewallConfigJob)
