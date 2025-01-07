"""API serializers for nautobot_firewall_models."""

from nautobot.apps.api import NautobotModelSerializer, TaggedModelSerializerMixin

from nautobot_firewall_models import models


class IPRangeSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):  # pylint: disable=too-many-ancestors
    """IPRange Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.IPRange
        fields = "__all__"

        # Option for disabling write for certain fields:
        # read_only_fields = []
