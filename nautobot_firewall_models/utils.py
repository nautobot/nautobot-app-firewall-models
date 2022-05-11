"""Help funcs for firewall models plugin."""
from django.conf import settings
from nautobot.extras.models import Status


def get_default_status():
    """Returns a default status value basedo n plugin config."""
    status_name = settings.PLUGINS_CONFIG.get("nautobot_firewall_models", {}).get("status_name", "Active")
    return Status.objects.get(name=status_name)
