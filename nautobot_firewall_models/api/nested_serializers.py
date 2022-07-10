"""Nested serializers."""
from nautobot.core.api import WritableNestedSerializer
from rest_framework.serializers import HyperlinkedIdentityField

from nautobot_firewall_models import models


class NestedFQDNSerializer(WritableNestedSerializer):
    """Nested serializer for FQDN."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_firewall_models-api:fqdn-detail")

    class Meta:
        """Meta attributes."""

        model = models.FQDN
        fields = ["id", "url", "name"]


class NestedIPRangeSerializer(WritableNestedSerializer):
    """Nested serializer for IPRange."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_firewall_models-api:fqdn-detail")

    class Meta:
        """Meta attributes."""

        model = models.IPRange
        fields = ["id", "url", "start_address", "end_address"]
