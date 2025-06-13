"""Django urlpatterns declaration for nautobot_firewall_models app."""

from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView
from nautobot.apps.urls import NautobotUIViewSetRouter

from nautobot_firewall_models import views

app_name = "nautobot_firewall_models"
router = NautobotUIViewSetRouter()
router.register("address-object", views.AddressObjectUIViewSet)
router.register("address-object-group", views.AddressObjectGroupUIViewSet)
router.register("application-object", views.ApplicationObjectUIViewSet)
router.register("application-object-group", views.ApplicationObjectGroupUIViewSet)
router.register("aerleon-policy", views.AerleonPolicyUIViewSet)
router.register("aerleon-policy-device", views.AerleonPolicyDeviceUIViewSet, basename="aerleonpolicy_devicedetail")
router.register("fqdn", views.FQDNUIViewSet)
router.register("ip-range", views.IPRangeUIViewSet)
router.register("nat-policy", views.NATPolicyUIViewSet)
router.register("nat-policy-rule", views.NATPolicyRuleUIViewSet)
router.register("policy", views.PolicyUIViewSet)
router.register("policy-rule", views.PolicyRuleUIViewSet)
router.register("service-object", views.ServiceObjectUIViewSet)
router.register("service-object-group", views.ServiceObjectGroupUIViewSet)
router.register("user-object", views.UserObjectUIViewSet)
router.register("user-object-group", views.UserObjectGroupUIViewSet)
router.register("zone", views.ZoneUIViewSet)

urlpatterns = [
    path("docs/", RedirectView.as_view(url=static("nautobot_firewall_models/docs/index.html")), name="docs"),
]

urlpatterns += router.urls
