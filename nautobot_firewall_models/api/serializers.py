"""API serializers for firewall models."""
from rest_framework import serializers

from nautobot.dcim.models import Device
from nautobot.apps.api import NautobotModelSerializer
from nautobot.extras.models import DynamicGroup
from nautobot.core.api.fields import NautobotHyperlinkedRelatedField

from nautobot_firewall_models import models


class IPRangeSerializer(NautobotModelSerializer):
    """IPRange Serializer."""

    start_address = serializers.CharField()
    end_address = serializers.CharField()

    class Meta:
        """Meta attributes."""

        model = models.IPRange
        fields = "__all__"


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

    address_objects = NautobotHyperlinkedRelatedField(
        queryset=models.AddressObject.objects.all(),
        many=True,
        required=False,
    )

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

    application_objects = NautobotHyperlinkedRelatedField(
        queryset=models.ApplicationObject.objects.all(),
        many=True,
        required=False,
    )

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

    service_objects = NautobotHyperlinkedRelatedField(
        queryset=models.ServiceObject.objects.all(),
        many=True,
        required=False,
    )

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

    user_objects = NautobotHyperlinkedRelatedField(
        queryset=models.UserObject.objects.all(),
        many=True,
        required=False,
    )

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

    # source
    source_users = NautobotHyperlinkedRelatedField(
        queryset=models.UserObject.objects.all(),
        many=True,
        required=False,
    )
    source_user_groups = NautobotHyperlinkedRelatedField(
        queryset=models.UserObjectGroup.objects.all(),
        many=True,
        required=False,
    )
    source_addresses = NautobotHyperlinkedRelatedField(
        queryset=models.AddressObject.objects.all(),
        many=True,
        required=False,
    )
    source_address_groups = NautobotHyperlinkedRelatedField(
        queryset=models.AddressObjectGroup.objects.all(),
        many=True,
        required=False,
    )
    source_services = NautobotHyperlinkedRelatedField(
        queryset=models.ServiceObject.objects.all(),
        many=True,
        required=False,
    )
    source_service_groups = NautobotHyperlinkedRelatedField(
        queryset=models.ServiceObjectGroup.objects.all(),
        many=True,
        required=False,
    )

    # destination
    applications = NautobotHyperlinkedRelatedField(
        queryset=models.ApplicationObject.objects.all(),
        many=True,
        required=False,
    )
    application_groups = NautobotHyperlinkedRelatedField(
        queryset=models.ApplicationObjectGroup.objects.all(),
        many=True,
        required=False,
    )
    destination_addresses = NautobotHyperlinkedRelatedField(
        queryset=models.AddressObject.objects.all(),
        many=True,
        required=False,
    )
    destination_address_groups = NautobotHyperlinkedRelatedField(
        queryset=models.AddressObjectGroup.objects.all(),
        many=True,
        required=False,
    )
    destination_services = NautobotHyperlinkedRelatedField(
        queryset=models.ServiceObject.objects.all(),
        many=True,
        required=False,
    )
    destination_service_groups = NautobotHyperlinkedRelatedField(
        queryset=models.ServiceObjectGroup.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        """Meta attributes."""

        model = models.PolicyRule
        fields = "__all__"


class PolicySerializer(NautobotModelSerializer):
    """Policy Serializer."""

    policy_rules = NautobotHyperlinkedRelatedField(
        queryset=models.PolicyRule.objects.all(),
        many=True,
        required=False,
    )
    assigned_devices = NautobotHyperlinkedRelatedField(
        queryset=Device.objects.all(),
        many=True,
        required=False,
    )
    assigned_dynamic_groups = NautobotHyperlinkedRelatedField(
        queryset=DynamicGroup.objects.all(),
        many=True,
        required=False,
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
        """Overload validate to pop field for custom m2m relationship."""
        # Remove custom fields data and tags (if any) prior to model validation
        attrs = data.copy()
        attrs.pop("policydevicem2m_set", None)
        attrs.pop("policydynamicgroupm2m_set", None)
        super().validate(attrs)
        return data


class NATPolicyRuleSerializer(NautobotModelSerializer):
    """PolicyRule Serializer."""

    # original source
    original_source_addresses = NautobotHyperlinkedRelatedField(
        queryset=models.AddressObject.objects.all(),
        many=True,
        required=False,
    )
    original_source_address_groups = NautobotHyperlinkedRelatedField(
        queryset=models.AddressObjectGroup.objects.all(),
        many=True,
        required=False,
    )
    original_source_services = NautobotHyperlinkedRelatedField(
        queryset=models.ServiceObject.objects.all(),
        many=True,
        required=False,
    )
    original_source_service_groups = NautobotHyperlinkedRelatedField(
        queryset=models.ServiceObjectGroup.objects.all(),
        many=True,
        required=False,
    )

    # translated source
    translated_source_addresses = NautobotHyperlinkedRelatedField(
        queryset=models.AddressObject.objects.all(),
        many=True,
        required=False,
    )
    translated_source_address_groups = NautobotHyperlinkedRelatedField(
        queryset=models.AddressObjectGroup.objects.all(),
        many=True,
        required=False,
    )
    translated_source_services = NautobotHyperlinkedRelatedField(
        queryset=models.ServiceObject.objects.all(),
        many=True,
        required=False,
    )
    translated_source_service_groups = NautobotHyperlinkedRelatedField(
        queryset=models.ServiceObjectGroup.objects.all(),
        many=True,
        required=False,
    )

    # original destination
    original_destination_addresses = NautobotHyperlinkedRelatedField(
        queryset=models.AddressObject.objects.all(),
        many=True,
        required=False,
    )
    original_destination_address_groups = NautobotHyperlinkedRelatedField(
        queryset=models.AddressObjectGroup.objects.all(),
        many=True,
        required=False,
    )
    original_destination_services = NautobotHyperlinkedRelatedField(
        queryset=models.ServiceObject.objects.all(),
        many=True,
        required=False,
    )
    original_destination_service_groups = NautobotHyperlinkedRelatedField(
        queryset=models.ServiceObjectGroup.objects.all(),
        many=True,
        required=False,
    )

    # translated destination
    translated_destination_addresses = NautobotHyperlinkedRelatedField(
        queryset=models.AddressObject.objects.all(),
        many=True,
        required=False,
    )
    translated_destination_address_groups = NautobotHyperlinkedRelatedField(
        queryset=models.AddressObjectGroup.objects.all(),
        many=True,
        required=False,
    )
    translated_destination_services = NautobotHyperlinkedRelatedField(
        queryset=models.ServiceObject.objects.all(),
        many=True,
        required=False,
    )
    translated_destination_service_groups = NautobotHyperlinkedRelatedField(
        queryset=models.ServiceObjectGroup.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        """Meta attributes."""

        model = models.NATPolicyRule
        fields = "__all__"


class NATPolicySerializer(NautobotModelSerializer):
    """NATPolicy Serializer."""

    nat_policy_rules = NautobotHyperlinkedRelatedField(
        queryset=models.NATPolicyRule.objects.all(),
        many=True,
        required=False,
    )
    assigned_devices = NautobotHyperlinkedRelatedField(
        queryset=Device.objects.all(),
        many=True,
        required=False,
    )
    assigned_dynamic_groups = NautobotHyperlinkedRelatedField(
        queryset=DynamicGroup.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        """Meta attributes."""

        model = models.NATPolicy
        fields = "__all__"

    def create(self, validated_data):
        """Overload create to account for custom m2m field."""
        assigned_devices = validated_data.pop("natpolicydevicem2m_set", None)
        assigned_dynamic_groups = validated_data.pop("natpolicydynamicgroupm2m_set", None)
        instance = super().create(validated_data)

        if assigned_devices is not None:
            return self._save_assigned_devices(instance, assigned_devices)
        if assigned_dynamic_groups is not None:
            return self._save_assigned_dynamic_groups(instance, assigned_dynamic_groups)

        return instance

    def update(self, instance, validated_data):
        """Overload create to account for update m2m field."""
        assigned_devices = validated_data.pop("natpolicydevicem2m_set", None)
        assigned_dynamic_groups = validated_data.pop("natpolicydynamicgroupm2m_set", None)

        instance = super().update(instance, validated_data)

        if assigned_devices is not None:
            return self._save_assigned_devices(instance, assigned_devices)
        if assigned_dynamic_groups is not None:
            return self._save_assigned_dynamic_groups(instance, assigned_dynamic_groups)

        return instance

    def _save_assigned_devices(self, instance, assigned_devices):
        """Helper function for custom m2m field."""
        instance.assigned_devices.clear()
        for dev in assigned_devices:
            models.NATPolicyDeviceM2M.objects.create(
                device=Device.objects.get(id=dev["device"].id),
                weight=dev.get("weight", None),
                policy=instance,
            )

        return instance

    def _save_assigned_dynamic_groups(self, instance, assigned_dynamic_groups):
        """Helper function for custom m2m field."""
        instance.assigned_dynamic_groups.clear()

        for d_g in assigned_dynamic_groups:
            models.NATPolicyDynamicGroupM2M.objects.create(
                dynamic_group=DynamicGroup.objects.get(id=d_g["dynamic_group"].id),
                weight=d_g.get("weight", None),
                policy=instance,
            )

        return instance

    def validate(self, data):
        """Overload validate to pop field for custom m2m relationship."""
        # Remove custom fields data and tags (if any) prior to model validation
        attrs = data.copy()
        attrs.pop("natpolicydevicem2m_set", None)
        attrs.pop("natpolicydynamicgroupm2m_set", None)
        super().validate(attrs)
        return data


class CapircaPolicySerializer(NautobotModelSerializer):
    """CapircaPolicy Serializer."""

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:nautobot_firewall_models-api:capircapolicy-detail"
    )

    class Meta:
        """Meta attributes."""

        model = models.CapircaPolicy
        fields = "__all__"
