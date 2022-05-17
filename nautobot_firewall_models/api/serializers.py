"""API serializers for firewall models."""

from nautobot.core.api import ValidatedModelSerializer, SerializedPKRelatedField
from nautobot.dcim.models import Device
from nautobot.extras.api.serializers import TaggedObjectSerializer
from nautobot.extras.models import DynamicGroup
from rest_framework import serializers

from nautobot_firewall_models import models


class IPRangeSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=too-many-ancestors
    """IPRange Serializer."""

    start_address = serializers.CharField()
    end_address = serializers.CharField()

    class Meta:
        """Meta attributes."""

        model = models.IPRange
        fields = "__all__"


class FQDNSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=too-many-ancestors
    """FQDN Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.FQDN
        fields = "__all__"


class AddressObjectSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=too-many-ancestors
    """AddressObject Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.AddressObject
        fields = "__all__"


class AddressObjectGroupSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=too-many-ancestors
    """AddressObjectGroup Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.AddressObjectGroup
        fields = "__all__"


class ServiceObjectSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=too-many-ancestors
    """ServiceObject Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.ServiceObject
        fields = "__all__"


class ServiceObjectGroupSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=too-many-ancestors
    """ServiceObjectGroup Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.ServiceObjectGroup
        fields = "__all__"


class UserObjectSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=too-many-ancestors
    """UserObject Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.UserObject
        fields = "__all__"


class UserObjectGroupSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=too-many-ancestors
    """UserObjectGroup Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.UserObjectGroup
        fields = "__all__"


class ZoneSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=too-many-ancestors
    """Zone Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.Zone
        fields = "__all__"


class PolicyRuleSerializer(TaggedObjectSerializer, ValidatedModelSerializer):
    # pylint: disable=too-many-ancestors
    """PolicyRule Serializer."""
    source_user = SerializedPKRelatedField(
        queryset=models.UserObject.objects.all(),
        serializer=UserObjectSerializer,
        required=False,
        many=True,
    )
    source_user_group = SerializedPKRelatedField(
        queryset=models.UserObjectGroup.objects.all(),
        serializer=UserObjectGroupSerializer,
        required=False,
        many=True,
    )
    source_address = SerializedPKRelatedField(
        queryset=models.AddressObject.objects.all(),
        serializer=AddressObjectSerializer,
        required=False,
        many=True,
    )
    source_address_group = SerializedPKRelatedField(
        queryset=models.AddressObjectGroup.objects.all(),
        serializer=AddressObjectGroupSerializer,
        required=False,
        many=True,
    )
    destination_address = SerializedPKRelatedField(
        queryset=models.AddressObject.objects.all(),
        serializer=AddressObjectSerializer,
        required=False,
        many=True,
    )
    destination_address_group = SerializedPKRelatedField(
        queryset=models.AddressObjectGroup.objects.all(),
        serializer=AddressObjectGroupSerializer,
        required=False,
        many=True,
    )
    service = SerializedPKRelatedField(
        queryset=models.ServiceObject.objects.all(),
        serializer=ServiceObjectSerializer,
        required=False,
        many=True,
    )
    service_group = SerializedPKRelatedField(
        queryset=models.ServiceObject.objects.all(),
        serializer=ServiceObjectGroupSerializer,
        required=False,
        many=True,
    )

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


class PolicyDeviceM2MNestedSerializer(serializers.ModelSerializer):
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
    # pylint: disable=too-many-ancestors
    """Policy Serializer."""

    policy_rules = PolicyRuleM2MNestedSerializer(many=True, required=False, source="policyrulem2m_set")
    assigned_devices = PolicyDeviceM2MNestedSerializer(many=True, required=False, source="policydevicem2m_set")
    assigned_dynamic_groups = PolicyDynamicGroupM2MNestedSerializer(
        many=True, required=False, source="policydynamicgroupm2m_set"
    )

    class Meta:
        """Meta attributes."""

        model = models.Policy
        fields = "__all__"

    def create(self, validated_data):
        """Overload create to account for custom m2m field."""
        policy_rules = validated_data.pop("policyrulem2m_set", None)
        assigned_devices = validated_data.pop("policydevicem2m_set", None)
        assigned_dynamic_groups = validated_data.pop("policydynamicgroupm2m_set", None)
        instance = super().create(validated_data)

        if policy_rules is not None:
            return self._save_policy_rules(instance, policy_rules)
        if assigned_devices is not None:
            return self._save_assigned_devices(instance, assigned_devices)
        if assigned_dynamic_groups is not None:
            return self._save_assigned_dynamic_groups(instance, assigned_dynamic_groups)

        return instance

    def update(self, instance, validated_data):
        """Overload create to account for update m2m field."""
        policy_rules = validated_data.pop("policyrulem2m_set", None)
        assigned_devices = validated_data.pop("policydevicem2m_set", None)
        assigned_dynamic_groups = validated_data.pop("policydynamicgroupm2m_set", None)

        instance = super().update(instance, validated_data)

        if policy_rules is not None:
            return self._save_policy_rules(instance, policy_rules)
        if assigned_devices is not None:
            return self._save_assigned_devices(instance, assigned_devices)
        if assigned_dynamic_groups is not None:
            return self._save_assigned_dynamic_groups(instance, assigned_dynamic_groups)

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

    def _save_assigned_devices(self, instance, assigned_devices):
        # pylint: disable=R0201
        """Helper function for custom m2m field."""
        instance.assigned_devices.clear()
        for dev in assigned_devices:
            models.PolicyDeviceM2M.objects.create(
                device=Device.objects.get(id=dev["device"].id),
                weight=dev.get("weight", None),
                policy=instance,
            )

        return instance

    def _save_assigned_dynamic_groups(self, instance, assigned_dynamic_groups):
        # pylint: disable=R0201
        """Helper function for custom m2m field."""
        instance.assigned_dynamic_groups.clear()

        for d_g in assigned_dynamic_groups:
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
