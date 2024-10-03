"""Help funcs for firewall models app."""

import json

from django.conf import settings
from django.utils.module_loading import import_string
from nautobot.core.models.utils import serialize_object_v2
from nautobot.extras.management import STATUS_COLOR_MAP, STATUS_DESCRIPTION_MAP
from nautobot.extras.models import Status
from rest_framework.renderers import JSONRenderer

from nautobot_firewall_models.constants import PLUGIN_CFG


def create_default_status():
    """Create the default status defined in the app config if it doesn't already exist."""
    status_name = PLUGIN_CFG.get("default_status")
    defaults = {"description": STATUS_DESCRIPTION_MAP.get(status_name, "")}
    if status_name in STATUS_COLOR_MAP:
        defaults["color"] = STATUS_COLOR_MAP[status_name]
    Status.objects.get_or_create(name=status_name, defaults=defaults)


def get_default_status():
    """Return the primary key of the default status defined in the app config."""
    status_name = settings.PLUGINS_CONFIG.get("nautobot_firewall_models", {}).get("default_status")
    default_status = Status.objects.filter(name=status_name)
    if not default_status.exists():
        create_default_status(None)

    return default_status.all().first().pk


def model_to_json(obj, cls=None):
    """Convenience method to convert object to json via a serializer."""
    if cls:
        # By default serialize_object_v2 will find a serializer, this is used to send in the serializer
        # you would prefer, via a `import_string` dotted path to the serializer
        return json.loads(JSONRenderer().render(import_string(cls)(obj, context={"request": None}).data))
    return json.loads(JSONRenderer().render(serialize_object_v2(obj)))
