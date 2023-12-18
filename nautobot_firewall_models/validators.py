"""Validators for app."""
import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_port(value):
    """Validates value is a port, port range, or port list."""
    for i in value.split(","):
        if i.isnumeric():
            continue
        if re.match(r"^\d*\-\d*$", i):
            continue
        if i is None or i == "":
            continue
        raise ValidationError(
            _("%(i)s is not a port number or port range."),
            params={"value": i},
        )


validate_port.message = "Must be a valid port, or port range."
