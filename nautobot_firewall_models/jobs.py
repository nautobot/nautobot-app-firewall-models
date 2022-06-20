"""Jobs to run backups, intended config, and compliance."""
import logging
from django.utils.timezone import make_aware

from nautobot.extras.jobs import Job, IntegerVar

from nautobot.dcim.models import Device
from nautobot_firewall_models.models.capirca_models import CapircaPolicy
from nautobot_firewall_models.models.core_models import Policy

LOGGER = logging.getLogger(__name__)


name = "Capirca Jobs"  # pylint: disable=invalid-name


class RunCapircaJob(Job):  # pylint disable=too-few-public-method
    """Class definition to use as Mixin for form definitions."""

    class Meta:
        """Meta object boilerplate for reservations."""

        name = "Generate FW Config via Capirca."
        description = "Generate FW Config via Capirca and update the models."
        commit_default = True

    def run(self, data, commit):
        """Run a job to remove legacy reservations."""
        queryset = []
        for policy in Policy.objects.all():
            for dyn in policy.assigned_dynamic_groups.get_queryset():
                if not queryset:
                    queryset = dyn.get_queryset()
                else:
                    queryset.union(dyn.get_queryset())
        for device in queryset:
            CapircaPolicy.objects.update_or_create(device=device)
            self.log_info(obj=device, message=f"{device} Updated")


jobs = [RunCapircaJob]
