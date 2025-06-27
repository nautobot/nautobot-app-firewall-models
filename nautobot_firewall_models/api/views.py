"""API views for nautobot_firewall_models."""

from nautobot.apps.api import ModelViewSet, NautobotModelViewSet

from nautobot_firewall_models import filters, models
from nautobot_firewall_models.api import serializers


class IPRangeViewSet(NautobotModelViewSet):
    """IPRange viewset."""

    queryset = models.IPRange.objects.all()
    serializer_class = serializers.IPRangeSerializer
    filterset_class = filters.IPRangeFilterSet


class FQDNViewSet(NautobotModelViewSet):
    """FQDN viewset."""

    queryset = models.FQDN.objects.all().prefetch_related("tags")
    serializer_class = serializers.FQDNSerializer
    filterset_class = filters.FQDNFilterSet


class AddressObjectViewSet(NautobotModelViewSet):
    """AddressObject viewset."""

    queryset = models.AddressObject.objects.all().prefetch_related("tags")
    serializer_class = serializers.AddressObjectSerializer
    filterset_class = filters.AddressObjectFilterSet


class AddressObjectGroupViewSet(NautobotModelViewSet):
    """AddressObjectGroup viewset."""

    queryset = models.AddressObjectGroup.objects.all().prefetch_related("tags")
    serializer_class = serializers.AddressObjectGroupSerializer
    filterset_class = filters.AddressObjectGroupFilterSet


class ApplicationObjectViewSet(NautobotModelViewSet):
    """ApplicationObject viewset."""

    queryset = models.ApplicationObject.objects.all().prefetch_related("tags")
    serializer_class = serializers.ApplicationObjectSerializer
    filterset_class = filters.ApplicationObjectFilterSet


class ApplicationObjectGroupViewSet(NautobotModelViewSet):
    """ApplicationObjectGroup viewset."""

    queryset = models.ApplicationObjectGroup.objects.all().prefetch_related("tags")
    serializer_class = serializers.ApplicationObjectGroupSerializer
    filterset_class = filters.ApplicationObjectGroupFilterSet


class ServiceObjectViewSet(NautobotModelViewSet):
    """ServiceObject viewset."""

    queryset = models.ServiceObject.objects.all().prefetch_related("tags")
    serializer_class = serializers.ServiceObjectSerializer
    filterset_class = filters.ServiceObjectFilterSet


class ServiceObjectGroupViewSet(NautobotModelViewSet):
    """ServiceObjectGroup viewset."""

    queryset = models.ServiceObjectGroup.objects.all().prefetch_related("tags")
    serializer_class = serializers.ServiceObjectGroupSerializer
    filterset_class = filters.ServiceObjectGroupFilterSet


class UserObjectViewSet(NautobotModelViewSet):
    """UserObject viewset."""

    queryset = models.UserObject.objects.all().prefetch_related("tags")
    serializer_class = serializers.UserObjectSerializer
    filterset_class = filters.UserObjectFilterSet


class UserObjectGroupViewSet(NautobotModelViewSet):
    """UserObjectGroup viewset."""

    queryset = models.UserObjectGroup.objects.all()
    serializer_class = serializers.UserObjectGroupSerializer
    filterset_class = filters.UserObjectGroupFilterSet


class ZoneViewSet(NautobotModelViewSet):
    """Zone viewset."""

    queryset = models.Zone.objects.all().prefetch_related("tags")
    serializer_class = serializers.ZoneSerializer
    filterset_class = filters.ZoneFilterSet


class PolicyRuleViewSet(NautobotModelViewSet):
    """PolicyRule viewset."""

    queryset = models.PolicyRule.objects.all().prefetch_related("tags")
    serializer_class = serializers.PolicyRuleSerializer
    filterset_class = filters.PolicyRuleFilterSet


class PolicyViewSet(NautobotModelViewSet):
    """Policy viewset."""

    queryset = models.Policy.objects.all().prefetch_related("tags")
    serializer_class = serializers.PolicySerializer
    filterset_class = filters.PolicyFilterSet


class NATPolicyRuleViewSet(NautobotModelViewSet):
    """NATPolicyRule viewset."""

    queryset = models.NATPolicyRule.objects.all().prefetch_related("tags")
    serializer_class = serializers.NATPolicyRuleSerializer
    filterset_class = filters.NATPolicyRuleFilterSet


class NATPolicyViewSet(NautobotModelViewSet):
    """NATPolicy viewset."""

    queryset = models.NATPolicy.objects.all().prefetch_related("tags")
    serializer_class = serializers.NATPolicySerializer
    filterset_class = filters.NATPolicyFilterSet


class AerleonPolicyViewSet(ModelViewSet):
    """AerleonPolicy viewset."""

    queryset = models.AerleonPolicy.objects.all().prefetch_related("tags")
    serializer_class = serializers.AerleonPolicySerializer
    filterset_class = filters.AerleonPolicyFilterSet


###########################
# Through Models
###########################


class PolicyDeviceM2MViewSet(ModelViewSet):
    """PolicyDeviceM2M viewset."""

    queryset = models.PolicyDeviceM2M.objects.all()
    serializer_class = serializers.PolicyDeviceM2MSerializer
    filterset_class = filters.PolicyDeviceM2MFilterSet


class PolicyVirtualMachineM2MViewSet(ModelViewSet):
    """PolicyVirtualMachineM2M viewset."""

    queryset = models.PolicyVirtualMachineM2M.objects.all()
    serializer_class = serializers.PolicyVirtualMachineM2MSerializer
    filterset_class = filters.PolicyVirtualMachineM2MFilterSet


class PolicyDynamicGroupM2MViewSet(ModelViewSet):
    """PolicyDynamicGroupM2M viewset."""

    queryset = models.PolicyDynamicGroupM2M.objects.all()
    serializer_class = serializers.PolicyDynamicGroupM2MSerializer
    filterset_class = filters.PolicyDynamicGroupM2MFilterSet


class NATPolicyDeviceM2MViewSet(ModelViewSet):
    """NATPolicyDeviceM2M viewset."""

    queryset = models.NATPolicyDeviceM2M.objects.all()
    serializer_class = serializers.NATPolicyDeviceM2MSerializer
    filterset_class = filters.NATPolicyDeviceM2MFilterSet


class NATPolicyDynamicGroupM2MViewSet(ModelViewSet):
    """NATPolicyDynamicGroupM2M viewset."""

    queryset = models.NATPolicyDynamicGroupM2M.objects.all()
    serializer_class = serializers.NATPolicyDynamicGroupM2MSerializer
    filterset_class = filters.NATPolicyDynamicGroupM2MFilterSet
