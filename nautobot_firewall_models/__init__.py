"""App declaration for nautobot_firewall_models."""

# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
from importlib import metadata

from nautobot.apps import NautobotAppConfig
from nautobot.core.signals import nautobot_database_ready

__version__ = metadata.version(__name__)


class NautobotFirewallModelsConfig(NautobotAppConfig):
    """App configuration for the nautobot_firewall_models app."""

    name = "nautobot_firewall_models"
    verbose_name = "Firewall & Security Models"
    version = __version__
    author = "Network to Code, LLC"
    description = "Nautobot App to model firewall and security objects. Allows users to model policies in a vendor-neutral manner and use that data to drive network security automation."
    base_url = "firewall"
    required_settings = []
    default_settings = {
        "aerleon_remark_pass": True,
        "aerleon_os_map": {},
        "allowed_status": ["Active"],
        "default_status": "Active",
        "protect_on_delete": True,
    }
    docs_view_name = "plugins:nautobot_firewall_models:docs"

    def ready(self):
        """Register custom signals."""
        import nautobot_firewall_models.signals  # pylint: disable=import-outside-toplevel

        nautobot_database_ready.connect(nautobot_firewall_models.signals.create_configured_statuses_signal, sender=self)
        nautobot_database_ready.connect(nautobot_firewall_models.signals.associate_statuses_signal, sender=self)

        super().ready()


config = NautobotFirewallModelsConfig  # pylint:disable=invalid-name
