"""API views for firewall models."""

from nautobot.core.api.views import ModelViewSet

from nautobot_firewall_models import filters, models
from nautobot_firewall_models.api import serializers


class IPRangeViewSet(ModelViewSet):
    """IPRange viewset."""

    queryset = models.IPRange.objects.all()
    serializer_class = serializers.IPRangeSerializer
    filterset_class = filters.IPRangeFilterSet


class FQDNViewSet(ModelViewSet):
    """FQDN viewset."""

    queryset = models.FQDN.objects.all()
    serializer_class = serializers.FQDNSerializer
    filterset_class = filters.FQDNFilterSet


class AddressObjectViewSet(ModelViewSet):
    """AddressObject viewset."""

    queryset = models.AddressObject.objects.all()
    serializer_class = serializers.AddressObjectSerializer
    filterset_class = filters.AddressObjectFilterSet


class AddressObjectGroupViewSet(ModelViewSet):
    """AddressObjectGroup viewset."""

    queryset = models.AddressObjectGroup.objects.all()
    serializer_class = serializers.AddressObjectGroupSerializer
    filterset_class = filters.AddressObjectGroupFilterSet


class ServiceObjectViewSet(ModelViewSet):
    """ServiceObject viewset."""

    queryset = models.ServiceObject.objects.all()
    serializer_class = serializers.ServiceObjectSerializer
    filterset_class = filters.ServiceObjectFilterSet


class ServiceObjectGroupViewSet(ModelViewSet):
    """ServiceObjectGroup viewset."""

    queryset = models.ServiceObjectGroup.objects.all()
    serializer_class = serializers.ServiceObjectGroupSerializer
    filterset_class = filters.ServiceObjectGroupFilterSet


class UserObjectViewSet(ModelViewSet):
    """UserObject viewset."""

    queryset = models.UserObject.objects.all()
    serializer_class = serializers.UserObjectSerializer
    filterset_class = filters.UserObjectFilterSet


class UserObjectGroupViewSet(ModelViewSet):
    """UserObjectGroup viewset."""

    queryset = models.UserObjectGroup.objects.all()
    serializer_class = serializers.UserObjectGroupSerializer
    filterset_class = filters.UserObjectGroupFilterSet


class ZoneViewSet(ModelViewSet):
    """Zone viewset."""

    queryset = models.Zone.objects.all()
    serializer_class = serializers.ZoneSerializer
    filterset_class = filters.ZoneFilterSet


class PolicyRuleViewSet(ModelViewSet):
    """PolicyRule viewset."""

    queryset = models.PolicyRule.objects.all()
    serializer_class = serializers.PolicyRuleSerializer
    filterset_class = filters.PolicyRuleFilterSet


class PolicyViewSet(ModelViewSet):
    """Policy viewset."""

    queryset = models.Policy.objects.all()
    serializer_class = serializers.PolicySerializer
    filterset_class = filters.PolicyFilterSet
