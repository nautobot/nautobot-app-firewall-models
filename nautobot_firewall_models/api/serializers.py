"""API serializers for firewall models."""

from nautobot.core.api import ValidatedModelSerializer
from nautobot.dcim.api.serializers import NestedDeviceSerializer
from nautobot.extras.api.serializers import TaggedObjectSerializer
from rest_framework import serializers

from nautobot_firewall_models import models


class IPRangeSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=R0901
    """IPRange Serializer."""

    start_address = serializers.CharField()
    end_address = serializers.CharField()

    class Meta:
        """Meta attributes."""

        model = models.IPRange
        fields = "__all__"


class FQDNSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=R0901
    """FQDN Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.FQDN
        fields = "__all__"


class AddressObjectSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=R0901
    """AddressObject Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.AddressObject
        fields = "__all__"


class AddressObjectGroupSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=R0901
    """AddressObjectGroup Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.AddressObjectGroup
        fields = "__all__"


class AddressPolicyObjectSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=R0901
    """AddressPolicyObject Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.AddressPolicyObject
        fields = "__all__"


class ServiceObjectSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=R0901
    """ServiceObject Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.ServiceObject
        fields = "__all__"


class ServiceObjectGroupSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=R0901
    """ServiceObjectGroup Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.ServiceObjectGroup
        fields = "__all__"


class ServicePolicyObjectSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=R0901
    """ServicePolicyObject Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.ServicePolicyObject
        fields = "__all__"


class UserObjectSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=R0901
    """UserObject Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.UserObject
        fields = "__all__"


class UserObjectGroupSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=R0901
    """UserObjectGroup Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.UserObjectGroup
        fields = "__all__"


class UserPolicyObjectSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=R0901
    """UserPolicyObject Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.UserPolicyObject
        fields = "__all__"


class ZoneSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=R0901
    """Zone Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.Zone
        fields = "__all__"


class SourceSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=R0901
    """Source Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.Source
        fields = "__all__"


class DestinationSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=R0901
    """Destination Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.Destination
        fields = "__all__"


class PolicyRuleSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=R0901
    """PolicyRule Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.PolicyRule
        fields = "__all__"


class PolicyRuleM2MNestedSerializer(serializers.ModelSerializer):
    """PolicyRuleM2M NestedSerializer."""

    class Meta:
        """Meta attributes."""

        model = models.PolicyRuleM2M
        fields = ["rule", "index"]


class PolicySerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=R0901
    """Policy Serializer."""

    devices = NestedDeviceSerializer(many=True, required=False)
    policy_rules = PolicyRuleM2MNestedSerializer(many=True, required=False, source="policyrulem2m_set")

    class Meta:
        """Meta attributes."""

        model = models.Policy
        fields = "__all__"

    def create(self, validated_data):
        """Overload create to account for custom m2m field."""
        policy_rules = validated_data.pop("policyrulem2m_set", None)
        instance = super().create(validated_data)
        if policy_rules is not None:
            return self._save_policy_rules(instance, policy_rules)
        return instance

    def update(self, instance, validated_data):
        """Overload create to account for update m2m field."""
        policy_rules = validated_data.pop("policyrulem2m_set", None)

        instance = super().update(instance, validated_data)

        if policy_rules is not None:
            return self._save_policy_rules(instance, policy_rules)
        return instance

    def _save_policy_rules(self, instance, policy_rules):
        # pylint: disable=R0201
        """Helper function for custom m2m field."""
        if policy_rules:
            instance.policy_rules.clear()
            for p_r in policy_rules:
                models.PolicyRuleM2M.objects.create(
                    rule=models.PolicyRule.objects.get(id=p_r["rule"].id),
                    index=p_r.get("index", None),
                    policy=instance,
                )
        else:
            instance.policy_rules.clear()

        return instance

    def validate(self, data):
        # pylint: disable=R0201
        """Overload validate to pop field for custom m2m relationship."""
        # Remove custom fields data and tags (if any) prior to model validation
        attrs = data.copy()
        attrs.pop("policyrulem2m_set", None)
        super().validate(attrs)
        return data
