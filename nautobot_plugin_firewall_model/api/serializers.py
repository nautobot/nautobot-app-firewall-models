"""API serializers for firewall models."""

from nautobot.core.api.serializers import ValidatedModelSerializer
from rest_framework import serializers

from nautobot_plugin_firewall_model import models
from nautobot_plugin_firewall_model.choices import TCP_UDP_CHOICES


class IPRangeSerializer(ValidatedModelSerializer):
    """IPRange Serializer."""

    start_address = serializers.CharField()
    end_address = serializers.CharField()

    class Meta:
        """Meta attributes."""

        model = models.IPRange
        fields = "__all__"


class ZoneSerializer(ValidatedModelSerializer):
    """Zone Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.Zone
        fields = "__all__"


class AddressGroupSerializer(ValidatedModelSerializer):
    """AddressGroup Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.AddressGroup
        fields = "__all__"


class ProtocolSerializer(ValidatedModelSerializer):
    """Protocol Serializer."""

    tcp_udp = serializers.ChoiceField(choices=TCP_UDP_CHOICES, required=False)

    class Meta:
        """Meta attributes."""

        model = models.Protocol
        fields = "__all__"


class ServiceGroupSerializer(ValidatedModelSerializer):
    """ServiceGroup Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.ServiceGroup
        fields = "__all__"


class UserSerializer(ValidatedModelSerializer):
    """User Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.User
        fields = "__all__"


class UserGroupSerializer(ValidatedModelSerializer):
    """UserGroup Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.UserGroup
        fields = "__all__"


class SourceDestinationSerializer(ValidatedModelSerializer):
    """SourceDestination Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.SourceDestination
        fields = "__all__"


class TermSerializer(ValidatedModelSerializer):
    """Term Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.Term
        fields = "__all__"


class PolicySerializer(ValidatedModelSerializer):
    """Policy Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.Policy
        fields = "__all__"
