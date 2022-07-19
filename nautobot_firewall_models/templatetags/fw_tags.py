"""Add custom templatetags."""
from django import template

register = template.Library()


@register.filter()
def render_truncate(content, length=50):
    """Customer truncate, since the default Django one renders oddly."""
    suffix = "\n..."
    if not content or len(content) <= length:
        return content
    return " ".join(content[: length + 1].split(" ")[0:-1]) + suffix
