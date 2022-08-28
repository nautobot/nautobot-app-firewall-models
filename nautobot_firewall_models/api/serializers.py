"""API serializers for firewall models."""

from rest_framework import serializers

from nautobot.core.api import ValidatedModelSerializer, SerializedPKRelatedField
from nautobot.dcim.api.nested_serializers import NestedInterfaceSerializer
from nautobot.dcim.models import Device
from nautobot.extras.api.customfields import CustomFieldModelSerializer
from nautobot.extras.api.fields import StatusSerializerField
from nautobot.extras.api.serializers import (
    StatusModelSerializerMixin as _StatusModelSerializerMixin,
    TaggedObjectSerializer,
    NautobotModelSerializer,
)
from nautobot.extras.models import DynamicGroup, Status
from nautobot.ipam.models import IPAddress
from nautobot.ipam.api.nested_serializers import NestedIPAddressSerializer, NestedPrefixSerializer


from nautobot_firewall_models import models
from nautobot_firewall_models.api import nested_serializers


class StatusModelSerializerMixin(_StatusModelSerializerMixin):  # pylint: disable=abstract-method
    """Overloaded mixing to set status to optional.

    Args:
        _StatusModelSerializerMixin (obj): Mixin to aid in working with Status object relationships.
    """

    status = StatusSerializerField(queryset=Status.objects.all(), required=False)


class IPRangeSerializer(TaggedObjectSerializer, StatusModelSerializerMixin, NautobotModelSerializer):
    """IPRange Serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:nautobot_firewall_models-api:iprange-detail")
    start_address = serializers.CharField()
    end_address = serializers.CharField()

    class Meta:
        """Meta attributes."""

        model = models.IPRange
        fields = "__all__"


class FQDNSerializer(TaggedObjectSerializer, StatusModelSerializerMixin, NautobotModelSerializer):
    """FQDN Serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:nautobot_firewall_models-api:fqdn-detail")
    ip_addresses = SerializedPKRelatedField(
        queryset=IPAddress.objects.all(), serializer=NestedIPAddressSerializer, required=False, many=True
    )

    class Meta:
        """Meta attributes."""

        model = models.FQDN
        fields = "__all__"


class AddressObjectSerializer(TaggedObjectSerializer, StatusModelSerializerMixin, NautobotModelSerializer):
    """AddressObject Serializer."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_firewall_models-api:addressobject-detail"
    )
    ip_range = nested_serializers.NestedIPRangeSerializer(required=False)
    fqdn = nested_serializers.NestedFQDNSerializer(required=False)
    ip_address = NestedIPAddressSerializer(required=False)
    prefix = NestedPrefixSerializer(required=False)

    class Meta:
        """Meta attributes."""

        model = models.AddressObject
        fields = "__all__"


class AddressObjectGroupSerializer(TaggedObjectSerializer, StatusModelSerializerMixin, NautobotModelSerializer):
    """AddressObjectGroup Serializer."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_firewall_models-api:addressobjectgroup-detail"
    )
    address_objects = SerializedPKRelatedField(
        queryset=models.AddressObject.objects.all(), serializer=AddressObjectSerializer, required=False, many=True
    )

    class Meta:
        """Meta attributes."""

        model = models.AddressObjectGroup
        fields = "__all__"


class ServiceObjectSerializer(TaggedObjectSerializer, StatusModelSerializerMixin, NautobotModelSerializer):
    """ServiceObject Serializer."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_firewall_models-api:serviceobject-detail"
    )

    class Meta:
        """Meta attributes."""

        model = models.ServiceObject
        fields = "__all__"


class ServiceObjectGroupSerializer(TaggedObjectSerializer, StatusModelSerializerMixin, NautobotModelSerializer):
    """ServiceObjectGroup Serializer."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_firewall_models-api:serviceobjectgroup-detail"
    )
    service_objects = SerializedPKRelatedField(
        queryset=models.ServiceObject.objects.all(), serializer=ServiceObjectSerializer, required=False, many=True
    )

    ServiceObjectSerializer()

    class Meta:
        """Meta attributes."""

        model = models.ServiceObjectGroup
        fields = "__all__"


class UserObjectSerializer(TaggedObjectSerializer, StatusModelSerializerMixin, NautobotModelSerializer):
    """UserObject Serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:nautobot_firewall_models-api:userobject-detail")

    class Meta:
        """Meta attributes."""

        model = models.UserObject
        fields = "__all__"


class UserObjectGroupSerializer(TaggedObjectSerializer, StatusModelSerializerMixin, NautobotModelSerializer):
    """UserObjectGroup Serializer."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_firewall_models-api:userobjectgroup-detail"
    )
    user_objects = SerializedPKRelatedField(
        queryset=models.UserObject.objects.all(), serializer=UserObjectSerializer, required=False, many=True
    )

    class Meta:
        """Meta attributes."""

        model = models.UserObjectGroup
        fields = "__all__"


class ZoneSerializer(TaggedObjectSerializer, StatusModelSerializerMixin, NautobotModelSerializer):
    """Zone Serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:nautobot_firewall_models-api:zone-detail")
    interfaces = NestedInterfaceSerializer(required=False, many=True)

    class Meta:
        """Meta attributes."""

        model = models.Zone
        fields = "__all__"


class PolicyRuleSerializer(TaggedObjectSerializer, StatusModelSerializerMixin, NautobotModelSerializer):
    """PolicyRule Serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:nautobot_firewall_models-api:policyrule-detail")
    source_users = SerializedPKRelatedField(
        queryset=models.UserObject.objects.all(), serializer=UserObjectSerializer, required=False, many=True
    )
    source_user_groups = SerializedPKRelatedField(
        queryset=models.UserObjectGroup.objects.all(), serializer=UserObjectGroupSerializer, required=False, many=True
    )
    source_addresses = SerializedPKRelatedField(
        queryset=models.AddressObject.objects.all(), serializer=AddressObjectSerializer, required=False, many=True
    )
    source_address_groups = SerializedPKRelatedField(
        queryset=models.AddressObjectGroup.objects.all(),
        serializer=AddressObjectGroupSerializer,
        required=False,
        many=True,
    )
    source_zone = ZoneSerializer(required=False)
    destination_addresses = SerializedPKRelatedField(
        queryset=models.AddressObject.objects.all(), serializer=AddressObjectSerializer, required=False, many=True
    )
    destination_address_groups = SerializedPKRelatedField(
        queryset=models.AddressObjectGroup.objects.all(),
        serializer=AddressObjectGroupSerializer,
        required=False,
        many=True,
    )
    destination_zone = ZoneSerializer(required=False)
    destination_services = SerializedPKRelatedField(
        queryset=models.ServiceObject.objects.all(), serializer=ServiceObjectSerializer, required=False, many=True
    )
    destination_service_groups = SerializedPKRelatedField(
        queryset=models.ServiceObjectGroup.objects.all(),
        serializer=ServiceObjectGroupSerializer,
        required=False,
        many=True,
    )

    class Meta:
        """Meta attributes."""

        model = models.PolicyRule
        fields = "__all__"


class PolicyRuleM2MNestedSerializer(serializers.ModelSerializer):
    """PolicyRuleM2M NestedSerializer for create & update views."""

    class Meta:
        """Meta attributes."""

        model = models.PolicyRuleM2M
        fields = ["rule"]


class PolicyRuleM2MDeepNestedSerializer(PolicyRuleM2MNestedSerializer):
    """Overload for retrieve views."""

    rule = PolicyRuleSerializer(read_only=True)


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


class PolicySerializer(TaggedObjectSerializer, StatusModelSerializerMixin, NautobotModelSerializer):
    """Policy Serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:nautobot_firewall_models-api:policy-detail")
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
        assigned_devices = validated_data.pop("policydevicem2m_set", None)
        assigned_dynamic_groups = validated_data.pop("policydynamicgroupm2m_set", None)
        instance = super().create(validated_data)

        if assigned_devices is not None:
            return self._save_assigned_devices(instance, assigned_devices)
        if assigned_dynamic_groups is not None:
            return self._save_assigned_dynamic_groups(instance, assigned_dynamic_groups)

        return instance

    def update(self, instance, validated_data):
        """Overload create to account for update m2m field."""
        assigned_devices = validated_data.pop("policydevicem2m_set", None)
        assigned_dynamic_groups = validated_data.pop("policydynamicgroupm2m_set", None)

        instance = super().update(instance, validated_data)

        if assigned_devices is not None:
            return self._save_assigned_devices(instance, assigned_devices)
        if assigned_dynamic_groups is not None:
            return self._save_assigned_dynamic_groups(instance, assigned_dynamic_groups)

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
                weight=d_g.get("weight", None),
                policy=instance,
            )

        return instance

    def validate(self, data):
        # pylint: disable=R0201
        """Overload validate to pop field for custom m2m relationship."""
        # Remove custom fields data and tags (if any) prior to model validation
        attrs = data.copy()
        attrs.pop("policydevicem2m_set", None)
        attrs.pop("policydynamicgroupm2m_set", None)
        super().validate(attrs)
        return data


class PolicyDeepSerializer(PolicySerializer):
    """Overload for create & update views."""

    policy_rules = SerializedPKRelatedField(
        queryset=models.PolicyRule.objects.all(), serializer=PolicyRuleSerializer, required=False, many=True
    )


class CapircaPolicySerializer(TaggedObjectSerializer, CustomFieldModelSerializer, ValidatedModelSerializer):
    """CapircaPolicy Serializer."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_firewall_models-api:capircapolicy-detail"
    )

    class Meta:
        """Meta attributes."""

        model = models.CapircaPolicy
        fields = "__all__"
