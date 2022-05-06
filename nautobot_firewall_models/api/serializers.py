"""API serializers for firewall models."""

from nautobot.core.api import ValidatedModelSerializer
from nautobot.dcim.models import Device
from nautobot.extras.api.serializers import TaggedObjectSerializer
from nautobot.extras.models import DynamicGroup
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


class ZoneSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=R0901
    """Zone Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.Zone
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


class PolicyDeivceM2MNestedSerializer(serializers.ModelSerializer):
    """PolicyDeviceM2M NestedSerializer."""

    class Meta:
        """Meta attributes."""

        model = models.PolicyDeviceM2M
        fields = ["device", "weight"]


class PolicyDynamicGroupM2MNestedSerializer(serializers.ModelSerializer):
    """PolicyDynamicGroupM2M NestedSerializer."""

    class Meta:
        """Meta attributes."""

        model = models.PolicyDynamicGroupM2M
        fields = ["dynamic_group", "weight"]


class PolicySerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=R0901
    """Policy Serializer."""

    policy_rules = PolicyRuleM2MNestedSerializer(many=True, required=False, source="policyrulem2m_set")
    devices = PolicyDeivceM2MNestedSerializer(many=True, required=False, source="policydevicem2m_set")
    dynamic_groups = PolicyDynamicGroupM2MNestedSerializer(
        many=True, required=False, source="policydynamicgroupm2m_set"
    )

    class Meta:
        """Meta attributes."""

        model = models.Policy
        fields = "__all__"

    def create(self, validated_data):
        """Overload create to account for custom m2m field."""
        policy_rules = validated_data.pop("policyrulem2m_set", None)
        devices = validated_data.pop("policydevicem2m_set", None)
        dynamic_groups = validated_data.pop("policydynamicgroupm2m_set", None)
        instance = super().create(validated_data)

        if policy_rules is not None:
            return self._save_policy_rules(instance, policy_rules)
        if devices is not None:
            return self._save_devices(instance, devices)
        if dynamic_groups is not None:
            return self._save_dynamic_groups(instance, dynamic_groups)

        return instance

    def update(self, instance, validated_data):
        """Overload create to account for update m2m field."""
        policy_rules = validated_data.pop("policyrulem2m_set", None)
        devices = validated_data.pop("policydevicem2m_set", None)
        dynamic_groups = validated_data.pop("policydynamicgroupm2m_set", None)

        instance = super().update(instance, validated_data)

        if policy_rules is not None:
            return self._save_policy_rules(instance, policy_rules)
        if devices is not None:
            return self._save_devices(instance, devices)
        if dynamic_groups is not None:
            return self._save_dynamic_groups(instance, dynamic_groups)

        return instance

    def _save_policy_rules(self, instance, policy_rules):
        # pylint: disable=R0201
        """Helper function for custom m2m field."""
        instance.policy_rules.clear()
        for p_r in policy_rules:
            models.PolicyRuleM2M.objects.create(
                rule=models.PolicyRule.objects.get(id=p_r["rule"].id),
                index=p_r.get("index", None),
                policy=instance,
            )

        return instance

    def _save_devices(self, instance, devices):
        # pylint: disable=R0201
        """Helper function for custom m2m field."""
        instance.devices.clear()
        for dev in devices:
            models.PolicyDeviceM2M.objects.create(
                device=Device.objects.get(id=dev["device"].id),
                weight=dev.get("weight", None),
                policy=instance,
            )

        return instance

    def _save_dynamic_groups(self, instance, dynamic_groups):
        # pylint: disable=R0201
        """Helper function for custom m2m field."""
        instance.dynamic_groups.clear()

        for d_g in dynamic_groups:
            models.PolicyDynamicGroupM2M.objects.create(
                dynamic_group=DynamicGroup.objects.get(id=d_g["dynamic_group"].id),
                index=d_g.get("weight", None),
                policy=instance,
            )

        return instance

    def validate(self, data):
        # pylint: disable=R0201
        """Overload validate to pop field for custom m2m relationship."""
        # Remove custom fields data and tags (if any) prior to model validation
        attrs = data.copy()
        attrs.pop("policyrulem2m_set", None)
        attrs.pop("policydevicem2m_set", None)
        attrs.pop("policydynamicgroupm2m_set", None)
        super().validate(attrs)
        return data
