"""Help funcs for firewall models plugin."""
import json
from django.conf import settings
from rest_framework.renderers import JSONRenderer
from nautobot.extras.models import Status
from nautobot.utilities.utils import serialize_object_v2


def get_default_status():
    """Returns a default status value based on plugin config."""
    status_name = settings.PLUGINS_CONFIG.get("nautobot_firewall_models", {}).get("default_status", "active")
    return Status.objects.get(slug=status_name)


def model_to_json(obj):
    return json.loads(JSONRenderer().render(serialize_object_v2(obj)))
