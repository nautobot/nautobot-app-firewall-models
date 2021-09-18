"""Django API urlpatterns declaration for firewall model plugin."""

from nautobot.core.api import OrderedDefaultRouter

from nautobot_plugin_firewall_model.api import views


router = OrderedDefaultRouter()
router.register("ip-range", views.IPRangeViewSet)
router.register("zone", views.ZoneViewSet)
router.register("address-group", views.AddressGroupViewSet)
router.register("protocol", views.ProtocolViewSet)
router.register("service-group", views.ServiceGroupViewSet)
router.register("user", views.UserViewSet)
router.register("user-group", views.UserGroupViewSet)
router.register("source-destination", views.SourceDestinationViewSet)
router.register("term", views.TermViewSet)
router.register("policy", views.PolicyViewSet)

urlpatterns = router.urls
