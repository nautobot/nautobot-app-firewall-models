"""Django API urlpatterns declaration for firewall model plugin."""

from nautobot.core.api import OrderedDefaultRouter

from nautobot_firewall_models.api import views


router = OrderedDefaultRouter()
router.register("ip-range", views.IPRangeViewSet)
router.register("fqdn", views.FQDNViewSet)
router.register("address-object", views.AddressObjectViewSet)
router.register("address-object-group", views.AddressObjectGroupViewSet)
router.register("service-object", views.ServiceObjectViewSet)
router.register("service-object-group", views.ServiceObjectGroupViewSet)
router.register("user-object", views.UserObjectViewSet)
router.register("user-object-group", views.UserObjectGroupViewSet)
router.register("zone", views.ZoneViewSet)
router.register("policy-rule", views.PolicyRuleViewSet)
router.register("policy", views.PolicyViewSet)

urlpatterns = router.urls
