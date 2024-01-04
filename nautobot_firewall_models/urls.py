"""Django urlpatterns declaration for nautobot_firewall_models app."""

from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView
from nautobot.core.views.routers import NautobotUIViewSetRouter

from nautobot_firewall_models import viewsets

router = NautobotUIViewSetRouter()
router.register("address-object", viewsets.AddressObjectUIViewSet)
router.register("address-object-group", viewsets.AddressObjectGroupUIViewSet)
router.register("application-object", viewsets.ApplicationObjectUIViewSet)
router.register("application-object-group", viewsets.ApplicationObjectGroupUIViewSet)
router.register("capirca-policy", viewsets.CapircaPolicyUIViewSet)
router.register("capirca-policy-device", viewsets.CapircaPolicyDeviceUIViewSet, basename="capircapolicy_devicedetail")
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
    path(
        "docs/",
        RedirectView.as_view(url=static("nautobot_firewall_models/docs/index.html")),
        name="docs",
    ),
]
urlpatterns += router.urls
