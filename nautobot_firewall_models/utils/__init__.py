"""Help funcs for firewall models app."""

import json
import re
import unicodedata

from django.apps import apps as django_apps
from django.contrib.contenttypes.models import ContentType
from django.utils.module_loading import import_string
from nautobot.core.models.utils import serialize_object_v2
from nautobot.extras.management import STATUS_COLOR_MAP, STATUS_DESCRIPTION_MAP
from rest_framework.renderers import JSONRenderer

from nautobot_firewall_models.constants import ALLOW_STATUS, PLUGIN_CFG

# pylint: disable=too-many-instance-attributes,too-many-locals


def _create_status(status_name, apps=django_apps):
    """Create a status with the given name, using nautobot default description and color if applicable."""
    Status = apps.get_model("extras.Status")  # pylint: disable=invalid-name
    defaults = {"description": STATUS_DESCRIPTION_MAP.get(status_name, "")}
    if status_name in STATUS_COLOR_MAP:
        defaults["color"] = STATUS_COLOR_MAP[status_name]
    status, _ = Status.objects.get_or_create(name=status_name, defaults=defaults)

    # Add the status to all firewall models with a status field
    content_types = get_firewall_models_with_status_field(apps=apps)
    status.content_types.add(*content_types)


def create_configured_statuses(apps=django_apps):
    """Create the configured statuses (default_status and allowed_status) for the firewall app if they don't already exist."""
    for status_name in get_configured_status_names():
        _create_status(status_name, apps=apps)


def create_default_status(apps=django_apps):
    """Create the default_status defined in the app config if it doesn't already exist."""
    default_status_name = PLUGIN_CFG.get("default_status")
    _create_status(default_status_name, apps=apps)


def get_configured_status_names():
    """Retrieve the names of the configured statuses (default_status and allowed_status) from the firewall app config."""
    configured_status_names = PLUGIN_CFG.get("allowed_status")
    if isinstance(configured_status_names, str):
        configured_status_names = [configured_status_names]
    return configured_status_names + [get_default_status_name()]


def get_default_status(apps=django_apps):
    """
    Return the primary key of the default status defined in the firewall app config.

    Creates the default status if it doesn't exist. Used by the firewall models for the status field default.
    """
    Status = apps.get_model("extras.Status")  # pylint: disable=invalid-name
    default_status_name = PLUGIN_CFG.get("default_status")
    default_status = Status.objects.filter(name=default_status_name)
    if not default_status.exists():
        create_default_status()

    return default_status.all().first().pk


def get_default_status_name():
    """Return the name of the default status defined in the firewall app config."""
    default_status_name = PLUGIN_CFG.get("default_status")
    return default_status_name


def get_firewall_models_with_status_field(apps=django_apps):
    """Return a list of content types for all firewall models that have a status field. Usable in migrations."""
    model_content_types = []
    _ContentType = apps.get_model("contenttypes.ContentType")  # pylint: disable=invalid-name
    for model in apps.get_app_config("nautobot_firewall_models").get_models():
        if hasattr(model, "status"):
            ct = _ContentType.objects.get_for_model(model)  # pylint: disable=invalid-name
            model_content_types.append(ct)

    return model_content_types


def model_to_json(obj, cls=None):
    """Convenience method to convert object to json via a serializer."""
    if cls:
        # By default serialize_object_v2 will find a serializer, this is used to send in the serializer
        # you would prefer, via a `import_string` dotted path to the serializer
        return json.loads(JSONRenderer().render(import_string(cls)(obj, context={"request": None}).data))
    return json.loads(JSONRenderer().render(serialize_object_v2(obj)))


def _slugify(value):
    """
    Taken from Django's implementation of slugify, to allow for capital letters.

    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value)
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def _list_slugify(values):
    """Function to go through list of names and slugify them."""
    return sorted([_slugify(i) for i in values])


def _clean_list(_list, remove_empty=False):
    """Remove duplicates and conditionally empty, such as None, in a list."""
    if remove_empty:
        _list = [i for i in _list if i]
    _list = list(set(_list))
    return sorted(_list)


def _get_instance_from_dict(obj):
    """Get DB object from serialized json."""
    if isinstance(obj, dict) and obj.get("id") and obj.get("object_type"):
        app, model = obj["object_type"].split(".")
        obj = ContentType.objects.get(app_label=app, model=model).get_object_for_this_type(id=obj["id"])
    return obj


def _check_status(status):
    """Check if status is active or as provided via plugin settings. If nothing, it is always good."""
    if not isinstance(status, str):
        status = _get_instance_from_dict(status).status.name
    if len(ALLOW_STATUS) == 0 or status not in ALLOW_STATUS:
        return True
    return False
