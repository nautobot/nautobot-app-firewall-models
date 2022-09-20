"""Help funcs for firewall models plugin."""
import json
from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework.renderers import JSONRenderer
from nautobot.extras.models import Status
from nautobot.utilities.utils import serialize_object_v2


def get_default_status():
    """Returns a default status value based on plugin config."""
    status_name = settings.PLUGINS_CONFIG.get("nautobot_firewall_models", {}).get("default_status", "active")
    return Status.objects.get(slug=status_name).pk


def model_to_json(obj, cls=None):
    """Convenience method to convert object to json via a serializer."""
    if cls:
        # By default serialize_object_v2 will find a serializer, this is used to send in the serializer
        # you would prefer, via a `import_string` dotted path to the serializer
        return json.loads(JSONRenderer().render(import_string(cls)(obj, context={"request": None}).data))
    return json.loads(JSONRenderer().render(serialize_object_v2(obj)))
