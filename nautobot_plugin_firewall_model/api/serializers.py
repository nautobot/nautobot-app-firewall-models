"""API serializers for firewall models."""

from nautobot.core.api.serializers import ValidatedModelSerializer
from rest_framework import serializers

from nautobot_plugin_firewall_model import models, choices


class IPRangeSerializer(ValidatedModelSerializer):
    """IPRange Serializer."""

    start_address = serializers.CharField()
    end_address = serializers.CharField()

    class Meta:
        """Meta attributes."""

        model = models.IPRange
        fields = "__all__"


class FQDNSerializer(ValidatedModelSerializer):
    """FQDN Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.FQDN
        fields = "__all__"


class AddressObjectSerializer(ValidatedModelSerializer):
    """AddressObject Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.AddressObject
        fields = "__all__"


class AddressObjectGroupSerializer(ValidatedModelSerializer):
    """AddressObjectGroup Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.AddressObjectGroup
        fields = "__all__"


class AddressPolicyObjectSerializer(ValidatedModelSerializer):
    """AddressPolicyObject Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.AddressPolicyObject
        fields = "__all__"


class ServiceObjectSerializer(ValidatedModelSerializer):
    """ServiceObject Serializer."""

    ip_protocol = serializers.ChoiceField(choices=choices.IP_PROTOCOL_CHOICES, required=False)

    class Meta:
        """Meta attributes."""

        model = models.ServiceObject
        fields = "__all__"


class ServiceObjectGroupSerializer(ValidatedModelSerializer):
    """ServiceObjectGroup Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.ServiceObjectGroup
        fields = "__all__"


class ServicePolicyObjectSerializer(ValidatedModelSerializer):
    """ServicePolicyObject Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.ServicePolicyObject
        fields = "__all__"


class UserObjectSerializer(ValidatedModelSerializer):
    """UserObject Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.UserObject
        fields = "__all__"


class UserObjectGroupSerializer(ValidatedModelSerializer):
    """UserObjectGroup Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.UserObjectGroup
        fields = "__all__"


class UserPolicyObjectSerializer(ValidatedModelSerializer):
    """UserPolicyObject Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.UserPolicyObject
        fields = "__all__"


class ZoneSerializer(ValidatedModelSerializer):
    """Zone Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.Zone
        fields = "__all__"


class SourceSerializer(ValidatedModelSerializer):
    """Source Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.Source
        fields = "__all__"


class DestinationSerializer(ValidatedModelSerializer):
    """Destination Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.Destination
        fields = "__all__"


class PolicyRuleSerializer(ValidatedModelSerializer):
    """PolicyRule Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.PolicyRule
        fields = "__all__"


class PolicySerializer(ValidatedModelSerializer):
    """Policy Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.Policy
        fields = "__all__"
