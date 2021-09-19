"""API views for firewall models."""

from nautobot.core.api.views import ModelViewSet

from nautobot_plugin_firewall_model import filters, models
from nautobot_plugin_firewall_model.api import serializers


class IPRangeViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """IPRange viewset."""

    queryset = models.IPRange.objects.all()
    serializer_class = serializers.IPRangeSerializer
    filterset_class = filters.IPRangeFilter


class ZoneViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """Zone viewset."""

    queryset = models.Zone.objects.all()
    serializer_class = serializers.ZoneSerializer
    filterset_class = filters.ZoneFilter


class AddressGroupViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """AddressGroup viewset."""

    queryset = models.AddressGroup.objects.all()
    serializer_class = serializers.AddressGroupSerializer
    filterset_class = filters.AddressGroupFilter


class FQDNViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """AddressGroup viewset."""

    queryset = models.FQDN.objects.all()
    serializer_class = serializers.FQDNSerializer
    filterset_class = filters.FQDNFilter


class ProtocolViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """Protocol viewset."""

    queryset = models.Protocol.objects.all()
    serializer_class = serializers.ProtocolSerializer
    filterset_class = filters.ProtocolFilter


class ServiceGroupViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """ServiceGroup viewset."""

    queryset = models.ServiceGroup.objects.all()
    serializer_class = serializers.ServiceGroupSerializer
    filterset_class = filters.ServiceGroupFilter


class UserViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """User viewset."""

    queryset = models.User.objects.all()
    serializer_class = serializers.FirewallUserSerializer
    filterset_class = filters.UserFilter


class UserGroupViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """UserGroup viewset."""

    queryset = models.UserGroup.objects.all()
    serializer_class = serializers.UserGroupSerializer
    filterset_class = filters.UserGroupFilter


class SourceDestinationViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """SourceDestination viewset."""

    queryset = models.SourceDestination.objects.all()
    serializer_class = serializers.SourceDestinationSerializer
    filterset_class = filters.SourceDestinationFilter


class TermViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """Term viewset."""

    queryset = models.Term.objects.all()
    serializer_class = serializers.TermSerializer
    filterset_class = filters.TermFilter


class PolicyViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """Policy viewset."""

    queryset = models.Policy.objects.all()
    serializer_class = serializers.PolicySerializer
    filterset_class = filters.PolicyFilter
