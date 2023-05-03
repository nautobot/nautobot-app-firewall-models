"""Nested serializers."""
from nautobot.core.api import WritableNestedSerializer
from rest_framework.serializers import CharField, HyperlinkedIdentityField

from nautobot_firewall_models import models


class NestedApplicationSerializer(WritableNestedSerializer):
    """Nested serializer for FQDN."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_firewall_models-api:applicationobject-detail")

    class Meta:
        """Meta attributes."""

        model = models.FQDN
        fields = ["id", "url", "name"]


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
    start_address = CharField()
    end_address = CharField()

    class Meta:
        """Meta attributes."""

        model = models.IPRange
        fields = ["id", "url", "start_address", "end_address"]


class NestedZoneSerializer(WritableNestedSerializer):
    """Nested serializer for Zone."""

    url = HyperlinkedIdentityField(view_name="plugins-api:nautobot_firewall_models-api:zone-detail")

    class Meta:
        """Meta attributes."""

        model = models.Zone
        fields = ["id", "url", "name"]
