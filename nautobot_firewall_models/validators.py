"""Validators for plugin."""
import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_port(value):
    """Validates value is a port or port range."""
    if value.isnumeric():
        return
    if re.match(r"^\d*\-\d*$", value):
        return
    if value is None or value == "":
        return
    raise ValidationError(
        _("%(value)s is not a port number or port range."),
        params={"value": value},
    )
