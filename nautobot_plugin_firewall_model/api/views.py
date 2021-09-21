"""API views for firewall models."""

from nautobot.core.api.views import ModelViewSet

from nautobot_plugin_firewall_model import filters, models
from nautobot_plugin_firewall_model.api import serializers


class IPRangeViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """IPRange viewset."""

    queryset = models.IPRange.objects.all()
    serializer_class = serializers.IPRangeSerializer
    filterset_class = filters.IPRangeFilter


class FQDNViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """FQDN viewset."""

    queryset = models.FQDN.objects.all()
    serializer_class = serializers.FQDNSerializer
    filterset_class = filters.FQDNFilter


class AddressObjectViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """AddressObject viewset."""

    queryset = models.AddressObject.objects.all()
    serializer_class = serializers.AddressObjectSerializer
    filterset_class = filters.AddressObjectFilter


class AddressObjectGroupViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """AddressObjectGroup viewset."""

    queryset = models.AddressObjectGroup.objects.all()
    serializer_class = serializers.AddressObjectGroupSerializer
    filterset_class = filters.AddressObjectGroupFilter


class AddressPolicyObjectViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """AddressPolicyObject viewset."""

    queryset = models.AddressPolicyObject.objects.all()
    serializer_class = serializers.AddressPolicyObjectSerializer
    filterset_class = filters.AddressPolicyObjectFilter


class ServiceObjectViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """ServiceObject viewset."""

    queryset = models.ServiceObject.objects.all()
    serializer_class = serializers.ServiceObjectSerializer
    filterset_class = filters.ServiceObjectFilter


class ServiceObjectGroupViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """ServiceObjectGroup viewset."""

    queryset = models.ServiceObjectGroup.objects.all()
    serializer_class = serializers.ServiceObjectGroupSerializer
    filterset_class = filters.ServiceObjectGroupFilter


class ServicePolicyObjectViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """ServicePolicyObject viewset."""

    queryset = models.ServicePolicyObject.objects.all()
    serializer_class = serializers.ServicePolicyObjectSerializer
    filterset_class = filters.ServicePolicyObjectFilter


class UserObjectViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """UserObject viewset."""

    queryset = models.UserObject.objects.all()
    serializer_class = serializers.UserObjectSerializer
    filterset_class = filters.UserObjectFilter


class UserObjectGroupViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """UserObjectGroup viewset."""

    queryset = models.UserObjectGroup.objects.all()
    serializer_class = serializers.UserObjectGroupSerializer
    filterset_class = filters.UserObjectGroupFilter


class UserPolicyObjectViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """UserPolicyObject viewset."""

    queryset = models.UserPolicyObject.objects.all()
    serializer_class = serializers.UserPolicyObjectSerializer
    filterset_class = filters.UserPolicyObjectFilter


class ZoneViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """Zone viewset."""

    queryset = models.Zone.objects.all()
    serializer_class = serializers.ZoneSerializer
    filterset_class = filters.ZoneFilter


class SourceViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """Source viewset."""

    queryset = models.Source.objects.all()
    serializer_class = serializers.SourceSerializer
    filterset_class = filters.SourceFilter


class DestinationViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """Destination viewset."""

    queryset = models.Destination.objects.all()
    serializer_class = serializers.DestinationSerializer
    filterset_class = filters.DestinationFilter


class PolicyRuleViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """PolicyRule viewset."""

    queryset = models.PolicyRule.objects.all()
    serializer_class = serializers.PolicyRuleSerializer
    filterset_class = filters.PolicyRuleFilter


class PolicyViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """Policy viewset."""

    queryset = models.Policy.objects.all()
    serializer_class = serializers.PolicySerializer
    filterset_class = filters.PolicyFilter
