"""API serializers for firewall models."""

from django.contrib.contenttypes.models import ContentType
from drf_yasg.utils import swagger_serializer_method
from nautobot.core.api import ContentTypeField
from nautobot.core.api.serializers import ValidatedModelSerializer
from nautobot.utilities.api import get_serializer_for_model
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

    tcp_udp = serializers.ChoiceField(choices=choices.TCP_UDP_CHOICES, required=False)

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


class FirewallUserSerializer(ValidatedModelSerializer):
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

    assigned_address_type = ContentTypeField(
        queryset=ContentType.objects.filter(choices.ADDRESS_ASSIGNMENT_MODELS),
        required=False,
        allow_null=True,
    )
    assigned_user_type = ContentTypeField(
        queryset=ContentType.objects.filter(choices.USER_ASSIGNMENT_MODELS),
        required=False,
        allow_null=True,
    )
    assigned_service_type = ContentTypeField(
        queryset=ContentType.objects.filter(choices.SERVICE_ASSIGNMENT_MODELS),
        required=False,
        allow_null=True,
    )
    address = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    service = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """Meta attributes."""

        model = models.SourceDestination
        fields = "__all__"

    @swagger_serializer_method(serializer_or_field=serializers.DictField)
    def get_address(self, obj):
        """Returns nested serializer if object is used."""
        if obj.address is None:
            return None
        serializer = get_serializer_for_model(obj.address, prefix="Nested")
        context = {"request": self.context["request"]}
        return serializer(obj.address, context=context).data

    @swagger_serializer_method(serializer_or_field=serializers.DictField)
    def get_user(self, obj):
        """Returns nested serializer if object is used."""
        if obj.user is None:
            return None
        serializer = get_serializer_for_model(obj.user, prefix="Nested")
        context = {"request": self.context["request"]}
        return serializer(obj.user, context=context).data

    @swagger_serializer_method(serializer_or_field=serializers.DictField)
    def get_service(self, obj):
        """Returns nested serializer if object is used."""
        if obj.service is None:
            return None
        serializer = get_serializer_for_model(obj.service, prefix="Nested")
        context = {"request": self.context["request"]}
        return serializer(obj.service, context=context).data


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


class FQDNSerializer(ValidatedModelSerializer):
    """FQDN Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.FQDN
        fields = "__all__"


class NestedServiceGroupSerializer(ServiceGroupSerializer):  # pylint: disable=too-many-ancestors
    """Placeholder for serializer."""


class NestedProtocolSerializer(ProtocolSerializer):  # pylint: disable=too-many-ancestors
    """Placeholder for serializer."""


class NestedFirewallUserSerializer(FirewallUserSerializer):  # pylint: disable=too-many-ancestors
    """Placeholder for serializer."""


class NestedUserGroupSerializer(UserGroupSerializer):  # pylint: disable=too-many-ancestors
    """Placeholder for serializer."""


class NestedAddressGroupSerializer(AddressGroupSerializer):  # pylint: disable=too-many-ancestors
    """Placeholder for serializer."""


class NestedIPRangeSerializer(IPRangeSerializer):  # pylint: disable=too-many-ancestors
    """Placeholder for serializer."""


class NestedFQDNSerializer(FQDNSerializer):  # pylint: disable=too-many-ancestors
    """Placeholder for serializer."""
