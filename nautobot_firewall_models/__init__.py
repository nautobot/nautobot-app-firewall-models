"""Plugin declaration for nautobot_firewall_models."""
# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
try:
    from importlib import metadata
except ImportError:
    # Python version < 3.8
    import importlib_metadata as metadata

__version__ = metadata.version(__name__)

from nautobot.extras.plugins import PluginConfig


class NautobotFirewallModelsConfig(PluginConfig):
    """Plugin configuration for the nautobot_firewall_models plugin."""

    name = "nautobot_firewall_models"
    verbose_name = "Firewall & Security Models"
    version = __version__
    author = "Network to Code, LLC"
    description = "Nautobot App to model firewall and security objects. Allows users to model policies in a vendor-neutral manner and use that data to drive network security automation."
    base_url = "firewall"
    required_settings = []
    min_version = "1.4.0"
    max_version = "1.9999"
    default_settings = {"capirca_remark_pass": True, "capirca_os_map": {}, "allowed_status": ["active"]}
    caching_config = {"*": {"timeout": 0}}
    docs_view_name = "plugins:nautobot_firewall_models:docs"


config = NautobotFirewallModelsConfig  # pylint:disable=invalid-name
