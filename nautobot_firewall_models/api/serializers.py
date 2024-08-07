"""API serializers for firewall models."""

from rest_framework import serializers
from nautobot.apps.api import NautobotModelSerializer, ValidatedModelSerializer

from nautobot_firewall_models import models


class IPRangeSerializer(NautobotModelSerializer):
    """IPRange Serializer."""

    start_address = serializers.CharField()
    end_address = serializers.CharField()

    class Meta:
        """Meta attributes."""

        model = models.IPRange
        fields = "__all__"

        # Omit the UniqueTogetherValidators that would be automatically added to validate (start_address, end_address, vrf).
        # This prevents vrf from being interpreted as a required field.
        validators = []

    def validate(self, data):
        """Custom validate method to enforce unique constraints on IPRange model."""
        # Validate uniqueness of (start_address, end_address, vrf) since we omitted the automatically-created validator above.
        start_address = data.get("start_address")
        end_address = data.get("end_address")
        vrf = data.get("vrf")
        if not any([start_address is not None, end_address is not None, vrf is not None]):
            return super().validate(data)

        # Use existing object's attributes for partial updates
        if self.instance:
            start_address = start_address or self.instance.start_address
            end_address = end_address or self.instance.end_address
            vrf = vrf or self.instance.vrf
            qs = models.IPRange.objects.exclude(pk=self.instance.pk)
        else:
            qs = models.IPRange.objects.all()

        if vrf is not None:
            if qs.filter(start_address=start_address, end_address=end_address, vrf=vrf).exists():
                raise serializers.ValidationError("The fields start_address, end_address, vrf must make a unique set.")
        else:
            if qs.filter(start_address=start_address, end_address=end_address, vrf__isnull=True).exists():
                raise serializers.ValidationError("The fields start_address, end_address must make a unique set.")

        return super().validate(data)


class FQDNSerializer(NautobotModelSerializer):
    """FQDN Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.FQDN
        fields = "__all__"


class AddressObjectSerializer(NautobotModelSerializer):
    """AddressObject Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.AddressObject
        fields = "__all__"


class AddressObjectGroupSerializer(NautobotModelSerializer):
    """AddressObjectGroup Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.AddressObjectGroup
        fields = "__all__"


class ApplicationObjectSerializer(NautobotModelSerializer):
    """ApplicationObject Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.ApplicationObject
        fields = "__all__"


class ApplicationObjectGroupSerializer(NautobotModelSerializer):
    """ApplicationObjectGroup Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.ApplicationObjectGroup
        fields = "__all__"


class ServiceObjectSerializer(NautobotModelSerializer):
    """ServiceObject Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.ServiceObject
        fields = "__all__"


class ServiceObjectGroupSerializer(NautobotModelSerializer):
    """ServiceObjectGroup Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.ServiceObjectGroup
        fields = "__all__"


class UserObjectSerializer(NautobotModelSerializer):
    """UserObject Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.UserObject
        fields = "__all__"


class UserObjectGroupSerializer(NautobotModelSerializer):
    """UserObjectGroup Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.UserObjectGroup
        fields = "__all__"


class ZoneSerializer(NautobotModelSerializer):
    """Zone Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.Zone
        fields = "__all__"


class PolicyRuleSerializer(NautobotModelSerializer):
    """PolicyRule Serializer."""

    index = serializers.IntegerField(required=False, default=None)

    class Meta:
        """Meta attributes."""

        model = models.PolicyRule
        fields = "__all__"


class PolicySerializer(NautobotModelSerializer):
    """Policy Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.Policy
        fields = "__all__"


class NATPolicyRuleSerializer(NautobotModelSerializer):
    """PolicyRule Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.NATPolicyRule
        fields = "__all__"


class NATPolicySerializer(NautobotModelSerializer):
    """NATPolicy Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.NATPolicy
        fields = "__all__"


class CapircaPolicySerializer(NautobotModelSerializer):
    """CapircaPolicy Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.CapircaPolicy
        fields = "__all__"


###########################
# Through Models
###########################


class PolicyDeviceM2MSerializer(ValidatedModelSerializer):
    """PolicyDeviceM2M Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.PolicyDeviceM2M
        fields = "__all__"


class PolicyDynamicGroupM2MSerializer(ValidatedModelSerializer):
    """PolicyDynamicGroupM2M Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.PolicyDynamicGroupM2M
        fields = "__all__"


class NATPolicyDeviceM2MSerializer(ValidatedModelSerializer):
    """NATPolicyDeviceM2M Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.NATPolicyDeviceM2M
        fields = "__all__"


class NATPolicyDynamicGroupM2MSerializer(ValidatedModelSerializer):
    """NATPolicyDynamicGroupM2M Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.NATPolicyDynamicGroupM2M
        fields = "__all__"
