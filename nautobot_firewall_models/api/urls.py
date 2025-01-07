"""Django API urlpatterns declaration for nautobot_firewall_models app."""

from nautobot.apps.api import OrderedDefaultRouter

from nautobot_firewall_models.api import views

router = OrderedDefaultRouter()
# add the name of your api endpoint, usually hyphenated model name in plural, e.g. "my-model-classes"
router.register("iprange", views.IPRangeViewSet)

urlpatterns = router.urls
