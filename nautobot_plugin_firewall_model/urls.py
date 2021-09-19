"""Django urlpatterns declaration for nautobot_plugin_firewall_model plugin."""

from django.urls import path
from nautobot.extras.views import ObjectChangeLogView

from nautobot_plugin_firewall_model import models
from nautobot_plugin_firewall_model.views import (
    fqdn,
    protocol,
    iprange,
    zone,
    address_group,
    service_group,
    user,
    user_group,
    source_destination,
    term,
    policy,
)

urlpatterns = [
    # FQDN URLs
    path("fqdn/", fqdn.FQDNListView.as_view(), name="fqdn_list"),
    # Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
    path("fqdn/add/", fqdn.FQDNCreateView.as_view(), name="fqdn_add"),
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
    # Protocol URLs
    path("protocol/", protocol.ProtocolListView.as_view(), name="protocol_list"),
    # Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
    path("protocol/add/", protocol.ProtocolCreateView.as_view(), name="protocol_add"),
    path("protocol/delete/", protocol.ProtocolBulkDeleteView.as_view(), name="protocol_bulk_delete"),
    path("protocol/edit/", protocol.ProtocolBulkEditView.as_view(), name="protocol_bulk_edit"),
    path("protocol/<uuid:pk>/", protocol.ProtocolView.as_view(), name="protocol"),
    path("protocol/<uuid:pk>/delete/", protocol.ProtocolDeleteView.as_view(), name="protocol_delete"),
    path("protocol/<uuid:pk>/edit/", protocol.ProtocolEditView.as_view(), name="protocol_edit"),
    path(
        "protocol/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="protocol_changelog",
        kwargs={"model": models.Protocol},
    ),
    # IPRange URLs
    path("ip-range/", iprange.IPRangeListView.as_view(), name="iprange_list"),
    # Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
    path("ip-range/add/", iprange.IPRangeCreateView.as_view(), name="iprange_add"),
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
    # Zone URLs
    path("zone/", zone.ZoneListView.as_view(), name="zone_list"),
    # Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
    path("zone/add/", zone.ZoneCreateView.as_view(), name="zone_add"),
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
    # AddressGroup URLs
    path("address-group/", address_group.AddressGroupListView.as_view(), name="addressgroup_list"),
    # Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
    path("address-group/add/", address_group.AddressGroupCreateView.as_view(), name="addressgroup_add"),
    path("address-group/delete/", address_group.AddressGroupBulkDeleteView.as_view(), name="addressgroup_bulk_delete"),
    path("address-group/edit/", address_group.AddressGroupBulkEditView.as_view(), name="addressgroup_bulk_edit"),
    path("address-group/<uuid:pk>/", address_group.AddressGroupView.as_view(), name="addressgroup"),
    path("address-group/<uuid:pk>/delete/", address_group.AddressGroupDeleteView.as_view(), name="addressgroup_delete"),
    path("address-group/<uuid:pk>/edit/", address_group.AddressGroupEditView.as_view(), name="addressgroup_edit"),
    path(
        "address-group/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="addressgroup_changelog",
        kwargs={"model": models.AddressGroup},
    ),
    # ServiceGroup URLs
    path("service-group/", service_group.ServiceGroupListView.as_view(), name="servicegroup_list"),
    # Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
    path("service-group/add/", service_group.ServiceGroupCreateView.as_view(), name="servicegroup_add"),
    path("service-group/delete/", service_group.ServiceGroupBulkDeleteView.as_view(), name="servicegroup_bulk_delete"),
    path("service-group/edit/", service_group.ServiceGroupBulkEditView.as_view(), name="servicegroup_bulk_edit"),
    path("service-group/<uuid:pk>/", service_group.ServiceGroupView.as_view(), name="servicegroup"),
    path("service-group/<uuid:pk>/delete/", service_group.ServiceGroupDeleteView.as_view(), name="servicegroup_delete"),
    path("service-group/<uuid:pk>/edit/", service_group.ServiceGroupEditView.as_view(), name="servicegroup_edit"),
    path(
        "service-group/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="servicegroup_changelog",
        kwargs={"model": models.ServiceGroup},
    ),
    # User URLs
    path("user/", user.UserListView.as_view(), name="user_list"),
    # Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
    path("user/add/", user.UserCreateView.as_view(), name="user_add"),
    path("user/delete/", user.UserBulkDeleteView.as_view(), name="user_bulk_delete"),
    path("user/edit/", user.UserBulkEditView.as_view(), name="user_bulk_edit"),
    path("user/<uuid:pk>/", user.UserView.as_view(), name="user"),
    path("user/<uuid:pk>/delete/", user.UserDeleteView.as_view(), name="user_delete"),
    path("user/<uuid:pk>/edit/", user.UserEditView.as_view(), name="user_edit"),
    path(
        "user/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="user_changelog",
        kwargs={"model": models.User},
    ),
    # UserGroup URLs
    path("user-group/", user_group.UserGroupListView.as_view(), name="usergroup_list"),
    # Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
    path("user-group/add/", user_group.UserGroupCreateView.as_view(), name="usergroup_add"),
    path("user-group/delete/", user_group.UserGroupBulkDeleteView.as_view(), name="usergroup_bulk_delete"),
    path("user-group/edit/", user_group.UserGroupBulkEditView.as_view(), name="usergroup_bulk_edit"),
    path("user-group/<uuid:pk>/", user_group.UserGroupView.as_view(), name="usergroup"),
    path("user-group/<uuid:pk>/delete/", user_group.UserGroupDeleteView.as_view(), name="usergroup_delete"),
    path("user-group/<uuid:pk>/edit/", user_group.UserGroupEditView.as_view(), name="usergroup_edit"),
    path(
        "user-group/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="usergroup_changelog",
        kwargs={"model": models.UserGroup},
    ),
    # SourceDestination URLs
    path("source-destination/", source_destination.SourceDestinationListView.as_view(), name="sourcedestination_list"),
    # Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
    path(
        "source-destination/add/",
        source_destination.SourceDestinationCreateView.as_view(),
        name="sourcedestination_add",
    ),
    path(
        "source-destination/delete/",
        source_destination.SourceDestinationBulkDeleteView.as_view(),
        name="sourcedestination_bulk_delete",
    ),
    path(
        "source-destination/edit/",
        source_destination.SourceDestinationBulkEditView.as_view(),
        name="sourcedestination_bulk_edit",
    ),
    path("source-destination/<uuid:pk>/", source_destination.SourceDestinationView.as_view(), name="sourcedestination"),
    path(
        "source-destination/<uuid:pk>/delete/",
        source_destination.SourceDestinationDeleteView.as_view(),
        name="sourcedestination_delete",
    ),
    path(
        "source-destination/<uuid:pk>/edit/",
        source_destination.SourceDestinationEditView.as_view(),
        name="sourcedestination_edit",
    ),
    path(
        "source-destination/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="sourcedestination_changelog",
        kwargs={"model": models.SourceDestination},
    ),
    # Term URLs
    path("term/", term.TermListView.as_view(), name="term_list"),
    # Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
    path("term/add/", term.TermCreateView.as_view(), name="term_add"),
    path("term/delete/", term.TermBulkDeleteView.as_view(), name="term_bulk_delete"),
    path("term/edit/", term.TermBulkEditView.as_view(), name="term_bulk_edit"),
    path("term/<uuid:pk>/", term.TermView.as_view(), name="term"),
    path("term/<uuid:pk>/delete/", term.TermDeleteView.as_view(), name="term_delete"),
    path("term/<uuid:pk>/edit/", term.TermEditView.as_view(), name="term_edit"),
    path(
        "term/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="term_changelog",
        kwargs={"model": models.Term},
    ),
    # Policy URLs
    path("policy/", policy.PolicyListView.as_view(), name="policy_list"),
    # Order is important for these URLs to work (add/delete/edit) to be before any that require uuid/slug
    path("policy/add/", policy.PolicyCreateView.as_view(), name="policy_add"),
    path("policy/delete/", policy.PolicyBulkDeleteView.as_view(), name="policy_bulk_delete"),
    path("policy/edit/", policy.PolicyBulkEditView.as_view(), name="policy_bulk_edit"),
    path("policy/<uuid:pk>/", policy.PolicyView.as_view(), name="policy"),
    path("policy/<uuid:pk>/delete/", policy.PolicyDeleteView.as_view(), name="policy_delete"),
    path("policy/<uuid:pk>/edit/", policy.PolicyEditView.as_view(), name="policy_edit"),
    path(
        "policy/<uuid:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="policy_changelog",
        kwargs={"model": models.Policy},
    ),
]
