"""API views for firewall models."""

from nautobot.core.api.views import ModelViewSet
from nautobot.core.settings_funcs import is_truthy
from nautobot.extras.api.views import NautobotModelViewSet

from nautobot_firewall_models import filters, models
from nautobot_firewall_models.api import serializers


class IPRangeViewSet(NautobotModelViewSet):
    """IPRange viewset."""

    queryset = models.IPRange.objects.all()
    serializer_class = serializers.IPRangeSerializer
    filterset_class = filters.IPRangeFilterSet


class FQDNViewSet(NautobotModelViewSet):
    """FQDN viewset."""

    queryset = models.FQDN.objects.all()
    serializer_class = serializers.FQDNSerializer
    filterset_class = filters.FQDNFilterSet


class AddressObjectViewSet(NautobotModelViewSet):
    """AddressObject viewset."""

    queryset = models.AddressObject.objects.all()
    serializer_class = serializers.AddressObjectSerializer
    filterset_class = filters.AddressObjectFilterSet


class AddressObjectGroupViewSet(NautobotModelViewSet):
    """AddressObjectGroup viewset."""

    queryset = models.AddressObjectGroup.objects.all()
    serializer_class = serializers.AddressObjectGroupSerializer
    filterset_class = filters.AddressObjectGroupFilterSet


class ServiceObjectViewSet(NautobotModelViewSet):
    """ServiceObject viewset."""

    queryset = models.ServiceObject.objects.all()
    serializer_class = serializers.ServiceObjectSerializer
    filterset_class = filters.ServiceObjectFilterSet


class ServiceObjectGroupViewSet(NautobotModelViewSet):
    """ServiceObjectGroup viewset."""

    queryset = models.ServiceObjectGroup.objects.all()
    serializer_class = serializers.ServiceObjectGroupSerializer
    filterset_class = filters.ServiceObjectGroupFilterSet


class UserObjectViewSet(NautobotModelViewSet):
    """UserObject viewset."""

    queryset = models.UserObject.objects.all()
    serializer_class = serializers.UserObjectSerializer
    filterset_class = filters.UserObjectFilterSet


class UserObjectGroupViewSet(NautobotModelViewSet):
    """UserObjectGroup viewset."""

    queryset = models.UserObjectGroup.objects.all()
    serializer_class = serializers.UserObjectGroupSerializer
    filterset_class = filters.UserObjectGroupFilterSet


class ZoneViewSet(NautobotModelViewSet):
    """Zone viewset."""

    queryset = models.Zone.objects.all()
    serializer_class = serializers.ZoneSerializer
    filterset_class = filters.ZoneFilterSet


class PolicyRuleViewSet(NautobotModelViewSet):
    """PolicyRule viewset."""

    queryset = models.PolicyRule.objects.all()
    serializer_class = serializers.PolicyRuleSerializer
    filterset_class = filters.PolicyRuleFilterSet


class PolicyViewSet(NautobotModelViewSet):
    """Policy viewset."""

    queryset = models.Policy.objects.all()
    serializer_class = serializers.PolicySerializer
    filterset_class = filters.PolicyFilterSet

    def get_serializer_class(self):
        """Overload for the ability to expand nested objects on retrieve view."""
        if self.action == "retrieve" and is_truthy(self.request.GET.get("deep", False)):
            self.serializer_class = serializers.PolicyDeepSerializer
        return super().get_serializer_class()


class CapircaPolicyViewSet(ModelViewSet):
    """CapircaPolicy viewset."""

    queryset = models.CapircaPolicy.objects.all()
    serializer_class = serializers.CapircaPolicySerializer
    filterset_class = filters.CapircaPolicyFilterSet
