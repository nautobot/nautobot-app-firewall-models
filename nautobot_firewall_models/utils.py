"""Help funcs for firewall models plugin."""
from django.conf import settings
from nautobot.extras.models import Status


def get_default_status():
    """Returns a default status value based on plugin config."""
    status_name = settings.PLUGINS_CONFIG.get("nautobot_firewall_models", {}).get("default_status", "active")
    return Status.objects.get(slug=status_name)
