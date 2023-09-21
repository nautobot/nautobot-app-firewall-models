"""Django urlpatterns declaration for nautobot_firewall_models plugin."""

from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView
from nautobot.core.views.routers import NautobotUIViewSetRouter

from nautobot_firewall_models.views import (
    policy,
    nat_policy,
    capirca_policy,
)

from nautobot_firewall_models import viewsets

router = NautobotUIViewSetRouter()
router.register("address-object", viewsets.AddressObjectUIViewSet)
router.register("address-object-group", viewsets.AddressObjectGroupUIViewSet)
router.register("application-object", viewsets.ApplicationObjectUIViewSet)
router.register("application-object-group", viewsets.ApplicationObjectGroupUIViewSet)
router.register("capirca-policy", viewsets.CapircaPolicyUIViewSet)
router.register("fqdn", viewsets.FQDNUIViewSet)
router.register("ip-range", viewsets.IPRangeUIViewSet)
router.register("nat-policy", viewsets.NATPolicyUIViewSet)
router.register("nat-policy-rule", viewsets.NATPolicyRuleUIViewSet)
router.register("policy", viewsets.PolicyUIViewSet)
router.register("policy-rule", viewsets.PolicyRuleUIViewSet)
router.register("service-object", viewsets.ServiceObjectUIViewSet)
router.register("service-object-group", viewsets.ServiceObjectGroupUIViewSet)
router.register("user-object", viewsets.UserObjectUIViewSet)
router.register("user-object-group", viewsets.UserObjectGroupUIViewSet)
router.register("zone", viewsets.ZoneUIViewSet)

urlpatterns = [
    # PolicyRule URLs
    path(
        "policy/<uuid:pk>/dynamic-groups/",
        policy.PolicyDynamicGroupWeight.as_view(),
        name="policy_set_dynamic_group_weight",
    ),
    path(
        "policy/<uuid:pk>/devices/",
        policy.PolicyDeviceWeight.as_view(),
        name="policy_set_device_weight",
    ),
    path(
        "nat-policy/<uuid:pk>/dynamic-groups/",
        nat_policy.NATPolicyDynamicGroupWeight.as_view(),
        name="natpolicy_set_dynamic_group_weight",
    ),
    path(
        "nat-policy/<uuid:pk>/devices/",
        nat_policy.NATPolicyDeviceWeight.as_view(),
        name="natpolicy_set_device_weight",
    ),
    path(
        "capirca-policy-device/<uuid:pk>",
        capirca_policy.CapircaPolicyDeviceView.as_view(),
        name="capircapolicy_devicedetail",
    ),
    path(
        "docs/",
        RedirectView.as_view(url=static("nautobot_firewall_models/docs/index.html")),
        name="docs",
    ),
]
urlpatterns += router.urls
