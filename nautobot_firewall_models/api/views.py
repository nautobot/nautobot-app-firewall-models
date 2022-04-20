"""API views for firewall models."""

from nautobot.core.api.views import ModelViewSet

from nautobot_firewall_models import filters, models
from nautobot_firewall_models.api import serializers


class IPRangeViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """IPRange viewset."""

    queryset = models.IPRange.objects.all()
    serializer_class = serializers.IPRangeSerializer
    filterset_class = filters.IPRangeFilterSet


class FQDNViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """FQDN viewset."""

    queryset = models.FQDN.objects.all()
    serializer_class = serializers.FQDNSerializer
    filterset_class = filters.FQDNFilterSet


class AddressObjectViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """AddressObject viewset."""

    queryset = models.AddressObject.objects.all()
    serializer_class = serializers.AddressObjectSerializer
    filterset_class = filters.AddressObjectFilterSet


class AddressObjectGroupViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """AddressObjectGroup viewset."""

    queryset = models.AddressObjectGroup.objects.all()
    serializer_class = serializers.AddressObjectGroupSerializer
    filterset_class = filters.AddressObjectGroupFilterSet


class AddressPolicyObjectViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """AddressPolicyObject viewset."""

    queryset = models.AddressPolicyObject.objects.all()
    serializer_class = serializers.AddressPolicyObjectSerializer
    filterset_class = filters.AddressPolicyObjectFilterSet


class ServiceObjectViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """ServiceObject viewset."""

    queryset = models.ServiceObject.objects.all()
    serializer_class = serializers.ServiceObjectSerializer
    filterset_class = filters.ServiceObjectFilterSet


class ServiceObjectGroupViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """ServiceObjectGroup viewset."""

    queryset = models.ServiceObjectGroup.objects.all()
    serializer_class = serializers.ServiceObjectGroupSerializer
    filterset_class = filters.ServiceObjectGroupFilterSet


class ServicePolicyObjectViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """ServicePolicyObject viewset."""

    queryset = models.ServicePolicyObject.objects.all()
    serializer_class = serializers.ServicePolicyObjectSerializer
    filterset_class = filters.ServicePolicyObjectFilterSet


class UserObjectViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """UserObject viewset."""

    queryset = models.UserObject.objects.all()
    serializer_class = serializers.UserObjectSerializer
    filterset_class = filters.UserObjectFilterSet


class UserObjectGroupViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """UserObjectGroup viewset."""

    queryset = models.UserObjectGroup.objects.all()
    serializer_class = serializers.UserObjectGroupSerializer
    filterset_class = filters.UserObjectGroupFilterSet


class UserPolicyObjectViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """UserPolicyObject viewset."""

    queryset = models.UserPolicyObject.objects.all()
    serializer_class = serializers.UserPolicyObjectSerializer
    filterset_class = filters.UserPolicyObjectFilterSet


class ZoneViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """Zone viewset."""

    queryset = models.Zone.objects.all()
    serializer_class = serializers.ZoneSerializer
    filterset_class = filters.ZoneFilterSet


class SourceDestinationViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """SourceDestination viewset."""

    queryset = models.SourceDestination.objects.all()
    serializer_class = serializers.SourceDestinationSerializer
    filterset_class = filters.SourceDestinationFilterSet


class PolicyRuleViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """PolicyRule viewset."""

    queryset = models.PolicyRule.objects.all()
    serializer_class = serializers.PolicyRuleSerializer
    filterset_class = filters.PolicyRuleFilterSet


class PolicyViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """Policy viewset."""

    queryset = models.Policy.objects.all()
    serializer_class = serializers.PolicySerializer
    filterset_class = filters.PolicyFilterSet
