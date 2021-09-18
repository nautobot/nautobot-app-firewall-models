"""Plugin declaration for nautobot_plugin_firewall_model."""
# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
try:
    from importlib import metadata
except ImportError:
    # Python version < 3.8
    import importlib_metadata as metadata

__version__ = metadata.version(__name__)

from nautobot.extras.plugins import PluginConfig


class NautobotPluginFirewallModelConfig(PluginConfig):
    """Plugin configuration for the nautobot_plugin_firewall_model plugin."""

    name = "nautobot_plugin_firewall_model"
    verbose_name = "Nautobot Plugin Firewall Model"
    version = __version__
    author = "Network to Code, LLC"
    description = "Nautobot plugin to model firweall objects.."
    base_url = "nautobot-plugin-firewall-model"
    required_settings = []
    min_version = "1.1.0"
    max_version = "1.9999"
    default_settings = {}
    caching_config = {}


config = NautobotPluginFirewallModelConfig  # pylint:disable=invalid-name
