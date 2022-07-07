"""Django urlpatterns declaration for nautobot_firewall_models plugin."""

from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView
from nautobot.extras.views import ObjectChangeLogView

from nautobot_firewall_models import models
from nautobot_firewall_models.views import (
    fqdn,
    iprange,
    zone,
    address_object,
    address_object_group,
    service_object,
    service_object_group,
    user_object,
    user_object_group,
    policy_rule,
    policy,
)

urlpatterns = [
    # FQDN URLs
    path("fqdn/", fqdn.FQDNListView.as_view(), name="fqdn_list"),
    # Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
    path("fqdn/add/", fqdn.FQDNEditView.as_view(), name="fqdn_add"),
    path("fqdn/delete/", fqdn.FQDNBulkDeleteView.as_view(), name="fqdn_bulk_delete"),
    path("fqdn/edit/", fqdn.FQDNBulkEditView.as_view(), name="fqdn_bulk_edit"),
    path("fqdn/<uuid:pk>/", fqdn.FQDNView.as_view(), name="fqdn"),
    path("fqdn/<uuid:pk>/delete/", fqdn.FQDNDeleteView.as_view(), name="fqdn_delete"),
    path("fqdn/<uuid:pk>/edit/", fqdn.FQDNEditView.as_view(), name="fqdn_edit"),
    path(
        "fqdn/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="fqdn_changelog",
        kwargs={"model": models.FQDN},
    ),
    # IPRange URLs
    path("ip-range/", iprange.IPRangeListView.as_view(), name="iprange_list"),
    # Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
    path("ip-range/add/", iprange.IPRangeEditView.as_view(), name="iprange_add"),
    path("ip-range/delete/", iprange.IPRangeBulkDeleteView.as_view(), name="iprange_bulk_delete"),
    path("ip-range/edit/", iprange.IPRangeBulkEditView.as_view(), name="iprange_bulk_edit"),
    path("ip-range/<uuid:pk>/", iprange.IPRangeView.as_view(), name="iprange"),
    path("ip-range/<uuid:pk>/delete/", iprange.IPRangeDeleteView.as_view(), name="iprange_delete"),
    path("ip-range/<uuid:pk>/edit/", iprange.IPRangeEditView.as_view(), name="iprange_edit"),
    path(
        "ip-range/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="iprange_changelog",
        kwargs={"model": models.IPRange},
    ),
    # AddressObject URLs
    path("address-object/", address_object.AddressObjectListView.as_view(), name="addressobject_list"),
    # Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
    path("address-object/add/", address_object.AddressObjectEditView.as_view(), name="addressobject_add"),
    path(
        "address-object/delete/", address_object.AddressObjectBulkDeleteView.as_view(), name="addressobject_bulk_delete"
    ),
    path("address-object/edit/", address_object.AddressObjectBulkEditView.as_view(), name="addressobject_bulk_edit"),
    path("address-object/<uuid:pk>/", address_object.AddressObjectView.as_view(), name="addressobject"),
    path(
        "address-object/<uuid:pk>/delete/",
        address_object.AddressObjectDeleteView.as_view(),
        name="addressobject_delete",
    ),
    path("address-object/<uuid:pk>/edit/", address_object.AddressObjectEditView.as_view(), name="addressobject_edit"),
    path(
        "address-object/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="addressobject_changelog",
        kwargs={"model": models.AddressObject},
    ),
    # AddressObjectGroup URLs
    path(
        "address-object-group/",
        address_object_group.AddressObjectGroupListView.as_view(),
        name="addressobjectgroup_list",
    ),
    # Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
    path(
        "address-object-group/add/",
        address_object_group.AddressObjectGroupEditView.as_view(),
        name="addressobjectgroup_add",
    ),
    path(
        "address-object-group/delete/",
        address_object_group.AddressObjectGroupBulkDeleteView.as_view(),
        name="addressobjectgroup_bulk_delete",
    ),
    path(
        "address-object-group/edit/",
        address_object_group.AddressObjectGroupBulkEditView.as_view(),
        name="addressobjectgroup_bulk_edit",
    ),
    path(
        "address-object-group/<uuid:pk>/",
        address_object_group.AddressObjectGroupView.as_view(),
        name="addressobjectgroup",
    ),
    path(
        "address-object-group/<uuid:pk>/delete/",
        address_object_group.AddressObjectGroupDeleteView.as_view(),
        name="addressobjectgroup_delete",
    ),
    path(
        "address-object-group/<uuid:pk>/edit/",
        address_object_group.AddressObjectGroupEditView.as_view(),
        name="addressobjectgroup_edit",
    ),
    path(
        "address-group/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="addressobjectgroup_changelog",
        kwargs={"model": models.AddressObjectGroup},
    ),
    # ServiceObject URLs
    path("service-object/", service_object.ServiceObjectListView.as_view(), name="serviceobject_list"),
    # Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
    path("service-object/add/", service_object.ServiceObjectEditView.as_view(), name="serviceobject_add"),
    path(
        "service-object/delete/", service_object.ServiceObjectBulkDeleteView.as_view(), name="serviceobject_bulk_delete"
    ),
    path("service-object/edit/", service_object.ServiceObjectBulkEditView.as_view(), name="serviceobject_bulk_edit"),
    path("service-object/<uuid:pk>/", service_object.ServiceObjectView.as_view(), name="serviceobject"),
    path(
        "service-object/<uuid:pk>/delete/",
        service_object.ServiceObjectDeleteView.as_view(),
        name="serviceobject_delete",
    ),
    path("service-object/<uuid:pk>/edit/", service_object.ServiceObjectEditView.as_view(), name="serviceobject_edit"),
    path(
        "service-object/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="serviceobject_changelog",
        kwargs={"model": models.ServiceObject},
    ),
    # ServiceObjectGroup URLs
    path(
        "service-object-group/",
        service_object_group.ServiceObjectGroupListView.as_view(),
        name="serviceobjectgroup_list",
    ),
    # Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
    path(
        "service-object-group/add/",
        service_object_group.ServiceObjectGroupEditView.as_view(),
        name="serviceobjectgroup_add",
    ),
    path(
        "service-object-group/delete/",
        service_object_group.ServiceObjectGroupBulkDeleteView.as_view(),
        name="serviceobjectgroup_bulk_delete",
    ),
    path(
        "service-object-group/edit/",
        service_object_group.ServiceObjectGroupBulkEditView.as_view(),
        name="serviceobjectgroup_bulk_edit",
    ),
    path(
        "service-object-group/<uuid:pk>/",
        service_object_group.ServiceObjectGroupView.as_view(),
        name="serviceobjectgroup",
    ),
    path(
        "service-object-group/<uuid:pk>/delete/",
        service_object_group.ServiceObjectGroupDeleteView.as_view(),
        name="serviceobjectgroup_delete",
    ),
    path(
        "service-object-group/<uuid:pk>/edit/",
        service_object_group.ServiceObjectGroupEditView.as_view(),
        name="serviceobjectgroup_edit",
    ),
    path(
        "service-object-group/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="serviceobjectgroup_changelog",
        kwargs={"model": models.ServiceObjectGroup},
    ),
    # UserObject URLs
    path("user-object/", user_object.UserObjectListView.as_view(), name="userobject_list"),
    # Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
    path("user-object/add/", user_object.UserObjectEditView.as_view(), name="userobject_add"),
    path("user-object/delete/", user_object.UserObjectBulkDeleteView.as_view(), name="userobject_bulk_delete"),
    path("user-object/edit/", user_object.UserObjectBulkEditView.as_view(), name="userobject_bulk_edit"),
    path("user-object/<uuid:pk>/", user_object.UserObjectView.as_view(), name="userobject"),
    path("user-object/<uuid:pk>/delete/", user_object.UserObjectDeleteView.as_view(), name="userobject_delete"),
    path("user-object/<uuid:pk>/edit/", user_object.UserObjectEditView.as_view(), name="userobject_edit"),
    path(
        "user-object/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="userobject_changelog",
        kwargs={"model": models.UserObject},
    ),
    # UserObjectGroup URLs
    path("user-object-group/", user_object_group.UserObjectGroupListView.as_view(), name="userobjectgroup_list"),
    # Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
    path("user-object-group/add/", user_object_group.UserObjectGroupEditView.as_view(), name="userobjectgroup_add"),
    path(
        "user-object-group/delete/",
        user_object_group.UserObjectGroupBulkDeleteView.as_view(),
        name="userobjectgroup_bulk_delete",
    ),
    path(
        "user-object-group/edit/",
        user_object_group.UserObjectGroupBulkEditView.as_view(),
        name="userobjectgroup_bulk_edit",
    ),
    path("user-object-group/<uuid:pk>/", user_object_group.UserObjectGroupView.as_view(), name="userobjectgroup"),
    path(
        "user-object-group/<uuid:pk>/delete/",
        user_object_group.UserObjectGroupDeleteView.as_view(),
        name="userobjectgroup_delete",
    ),
    path(
        "user-object-group/<uuid:pk>/edit/",
        user_object_group.UserObjectGroupEditView.as_view(),
        name="userobjectgroup_edit",
    ),
    path(
        "user-object-group/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="userobjectgroup_changelog",
        kwargs={"model": models.UserObjectGroup},
    ),
    # Zone URLs
    path("zone/", zone.ZoneListView.as_view(), name="zone_list"),
    # Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
    path("zone/add/", zone.ZoneEditView.as_view(), name="zone_add"),
    path("zone/delete/", zone.ZoneBulkDeleteView.as_view(), name="zone_bulk_delete"),
    path("zone/edit/", zone.ZoneBulkEditView.as_view(), name="zone_bulk_edit"),
    path("zone/<uuid:pk>/", zone.ZoneView.as_view(), name="zone"),
    path("zone/<uuid:pk>/delete/", zone.ZoneDeleteView.as_view(), name="zone_delete"),
    path("zone/<uuid:pk>/edit/", zone.ZoneEditView.as_view(), name="zone_edit"),
    path(
        "zone/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="zone_changelog",
        kwargs={"model": models.Zone},
    ),
    # PolicyRule URLs
    path("policy-rule/", policy_rule.PolicyRuleListView.as_view(), name="policyrule_list"),
    # Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
    path("policy-rule/add/", policy_rule.PolicyRuleEditView.as_view(), name="policyrule_add"),
    path("policy-rule/delete/", policy_rule.PolicyRuleBulkDeleteView.as_view(), name="policyrule_bulk_delete"),
    path("policy-rule/edit/", policy_rule.PolicyRuleBulkEditView.as_view(), name="policyrule_bulk_edit"),
    path("policy-rule/<uuid:pk>/", policy_rule.PolicyRuleView.as_view(), name="policyrule"),
    path("policy-rule/<uuid:pk>/delete/", policy_rule.PolicyRuleDeleteView.as_view(), name="policyrule_delete"),
    path("policy-rule/<uuid:pk>/edit/", policy_rule.PolicyRuleEditView.as_view(), name="policyrule_edit"),
    path(
        "policy-rule/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="policyrule_changelog",
        kwargs={"model": models.PolicyRule},
    ),
    # Policy URLs
    path("policy/", policy.PolicyListView.as_view(), name="policy_list"),
    # Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
    path("policy/add/", policy.PolicyEditView.as_view(), name="policy_add"),
    path("policy/delete/", policy.PolicyBulkDeleteView.as_view(), name="policy_bulk_delete"),
    path("policy/edit/", policy.PolicyBulkEditView.as_view(), name="policy_bulk_edit"),
    path("policy/<uuid:pk>/", policy.PolicyView.as_view(), name="policy"),
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
        "policy/<uuid:pk>/policy-rules/",
        policy.PolicyPolicyRuleIndex.as_view(),
        name="policy_set_policy_rule_index",
    ),
    path("policy/<uuid:pk>/delete/", policy.PolicyDeleteView.as_view(), name="policy_delete"),
    path("policy/<uuid:pk>/edit/", policy.PolicyEditView.as_view(), name="policy_edit"),
    path(
        "policy/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="policy_changelog",
        kwargs={"model": models.Policy},
    ),
    path(
        "docs/",
        RedirectView.as_view(url=static("nautobot_firewall_models/docs/index.html")),
        name="docs",
    ),
]
