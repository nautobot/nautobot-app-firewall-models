"""API views for nautobot_firewall_models."""

from nautobot.apps.api import NautobotModelViewSet

from nautobot_firewall_models import filters, models
from nautobot_firewall_models.api import serializers


class IPRangeViewSet(NautobotModelViewSet):  # pylint: disable=too-many-ancestors
    """IPRange viewset."""

    queryset = models.IPRange.objects.all()
    serializer_class = serializers.IPRangeSerializer
    filterset_class = filters.IPRangeFilterSet

    # Option for modifying the default HTTP methods:
    # http_method_names = ["get", "post", "put", "patch", "delete", "head", "options", "trace"]
