"""App declaration for nautobot_firewall_models."""

# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
from importlib import metadata

from nautobot.apps import NautobotAppConfig

__version__ = metadata.version(__name__)


class NautobotFirewallModelsConfig(NautobotAppConfig):
    """App configuration for the nautobot_firewall_models app."""

    name = "nautobot_firewall_models"
    verbose_name = "Nautobot Firewall Models"
    version = __version__
    author = "Network to Code, LLC"
    description = "Nautobot App to model firewall and security objects. Allows users to model policies in a vendor-neutral manner and use that data to drive network security automation."
    base_url = "firewall-models"
    required_settings = []
    min_version = "2.0.0"
    max_version = "2.9999"
    default_settings = {}
    caching_config = {}
    docs_view_name = "plugins:nautobot_firewall_models:docs"


config = NautobotFirewallModelsConfig  # pylint:disable=invalid-name
