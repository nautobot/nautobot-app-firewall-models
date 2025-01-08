"""Django API urlpatterns declaration for nautobot_firewall_models app."""

from nautobot.apps.api import OrderedDefaultRouter

from nautobot_firewall_models.api import views

router = OrderedDefaultRouter()
# add the name of your api endpoint, usually hyphenated model name in plural, e.g. "my-model-classes"
router.register("address-object", views.AddressObjectViewSet)
router.register("address-object-group", views.AddressObjectGroupViewSet)
router.register("application-object", views.ApplicationObjectViewSet)
router.register("application-object-group", views.ApplicationObjectGroupViewSet)
router.register("capirca-policy", views.CapircaPolicyViewSet)
router.register("fqdn", views.FQDNViewSet)
router.register("ip-range", views.IPRangeViewSet)
router.register("nat-policy-rule", views.NATPolicyRuleViewSet)
router.register("nat-policy", views.NATPolicyViewSet)
router.register("nat-policy-device-association", views.NATPolicyDeviceM2MViewSet)
router.register("nat-policy-dynamic-group-association", views.NATPolicyDynamicGroupM2MViewSet)
router.register("policy-rule", views.PolicyRuleViewSet)
router.register("policy", views.PolicyViewSet)
router.register("policy-device-association", views.PolicyDeviceM2MViewSet)
router.register("policy-dynamic-group-association", views.PolicyDynamicGroupM2MViewSet)
router.register("service-object", views.ServiceObjectViewSet)
router.register("service-object-group", views.ServiceObjectGroupViewSet)
router.register("user-object", views.UserObjectViewSet)
router.register("user-object-group", views.UserObjectGroupViewSet)
router.register("zone", views.ZoneViewSet)

urlpatterns = router.urls
