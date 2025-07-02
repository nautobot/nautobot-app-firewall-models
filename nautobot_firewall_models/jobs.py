"""Jobs to run backups, intended config, and compliance."""

from django.contrib.contenttypes.models import ContentType
from nautobot.core.celery import register_jobs
from nautobot.dcim.models import Device
from nautobot.extras.jobs import Job, MultiObjectVar, get_task_logger
from nautobot.virtualization.models import VirtualMachine

from nautobot_firewall_models.models import AerleonPolicy, Policy

logger = get_task_logger(__name__)

name = "Aerleon Jobs"  # pylint: disable=invalid-name


class RunAerleonJob(Job):  # pylint disable=too-few-public-method
    """Class definition to use as Mixin for form definitions."""

    devices = MultiObjectVar(model=Device, required=False)
    virtual_machines = MultiObjectVar(model=VirtualMachine, required=False)

    class Meta:
        """Meta object boilerplate for reservations."""

        name = "Generate FW Config via Aerleon."
        description = "Generate FW Config via Aerleon and update the models."
        commit_default = True
        has_sensitive_variables = False

    def run(self, devices, virtual_machines):  # pylint: disable=arguments-differ
        """Run a job to remove legacy reservations."""
        objects = set()

        # Note: devices and virtual_machines are QuerySets at this point.
        if devices or virtual_machines:
            if devices:
                objects.update(devices.all())
            if virtual_machines:
                objects.update(virtual_machines.all())
        else:
            # TODO: see if this logic can be optimized
            for policy in Policy.objects.all():
                for dyn in policy.assigned_dynamic_groups.get_queryset():
                    objects.update(dyn.members.all())
                for dev in policy.assigned_devices.all():
                    objects.add(dev)
                for vm in policy.assigned_virtual_machines.all():
                    objects.add(vm)

        for obj in objects:
            logger.debug("Running: `%s`", str(obj))
            ct = ContentType.objects.get_for_model(obj)
            AerleonPolicy.objects.update_or_create(content_type=ct, object_id=obj.id)
            logger.info("%s Updated", obj, extra={"object": obj})


jobs = [RunAerleonJob]
register_jobs(*jobs)
