"""App declaration for nautobot_firewall_models."""
# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
from importlib import metadata

__version__ = metadata.version(__name__)

from nautobot.apps import NautobotAppConfig


class NautobotFirewallModelsConfig(NautobotAppConfig):
    """App configuration for the nautobot_firewall_models app."""

    name = "nautobot_firewall_models"
    verbose_name = "Firewall & Security Models"
    version = __version__
    author = "Network to Code, LLC"
    description = "Nautobot App to model firewall and security objects. Allows users to model policies in a vendor-neutral manner and use that data to drive network security automation."
    base_url = "firewall"
    required_settings = []
    min_version = "2.0.0"
    max_version = "2.9999"
    default_settings = {
        "capirca_remark_pass": True,
        "capirca_os_map": {},
        "allowed_status": ["Active"],
        "protect_on_delete": True,
    }
    docs_view_name = "plugins:nautobot_firewall_models:docs"

    def ready(self):
        """Register custom signals."""
        import nautobot_firewall_models.signals  # noqa: F401, pylint: disable=import-outside-toplevel,unused-import

        super().ready()


config = NautobotFirewallModelsConfig  # pylint:disable=invalid-name
