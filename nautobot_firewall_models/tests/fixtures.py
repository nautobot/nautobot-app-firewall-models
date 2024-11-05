"""Create basic objects for use in test class setup."""

# ruff: noqa: F403, F405
from django.contrib.contenttypes.models import ContentType
from nautobot.dcim.models import Device, DeviceType, Location, LocationType, Manufacturer, Platform
from nautobot.extras.models import DynamicGroup, Job, Role
from nautobot.extras.models.statuses import Status
from nautobot.ipam.models import VRF, Namespace, Prefix
from nautobot.ipam.models import IPAddress as IPAddr
from nautobot.tenancy.models import Tenant, TenantGroup

from nautobot_firewall_models.models import *  # pylint: disable=unused-wildcard-import, wildcard-import


def create_ip_range():
    """Creates 3 IPRange objects."""
    status = Status.objects.get(name="Active")
    vrf, _ = VRF.objects.get_or_create(name="random_vrf")
    IPRange.objects.get_or_create(start_address="192.168.0.1", end_address="192.168.0.10", vrf=None, status=status)
    IPRange.objects.get_or_create(start_address="192.168.0.1", end_address="192.168.0.10", vrf=vrf, status=status)
    return IPRange.objects.get_or_create(start_address="192.168.0.11", end_address="192.168.0.20", status=status)[0]


def create_fqdn():
    """Creates 3 FQDN objects."""
    status = Status.objects.get(name="Active")
    FQDN.objects.get_or_create(name="test.dev", status=status)
    FQDN.objects.get_or_create(name="test.uat", status=status)
    return FQDN.objects.get_or_create(name="test.prod", status=status)[0]


def create_addr_obj():
    """Creates 3 of all objects."""
    # Core Models
    status = Status.objects.get(name="Active")
    namespace, _ = Namespace.objects.get_or_create(name="global")
    prefix, _ = Prefix.objects.get_or_create(network="10.0.0.0", prefix_length=24, namespace=namespace, status=status)
    ip_address, _ = IPAddr.objects.get_or_create(address="10.0.0.1", status=status, parent=prefix)

    # Plugin Models
    ip_range = create_ip_range()
    fqdn = create_fqdn()
    addr_obj1, _ = AddressObject.objects.get_or_create(name="printer", ip_range=ip_range, status=status)
    addr_obj2, _ = AddressObject.objects.get_or_create(name="voice", ip_address=ip_address, status=status)
    addr_obj3, _ = AddressObject.objects.get_or_create(name="storage", prefix=prefix, status=status)
    addr_obj4, _ = AddressObject.objects.get_or_create(name="server", fqdn=fqdn, status=status)
    return addr_obj1, addr_obj2, addr_obj3, addr_obj4


def create_addr_group():
    """Creates 3 of all objects."""
    status = Status.objects.get(name="Active")
    addr_obj1, addr_obj2, addr_obj3, addr_obj4 = create_addr_obj()
    addr_grp1, _ = AddressObjectGroup.objects.get_or_create(name="addr group1", status=status)
    addr_grp1.address_objects.set([addr_obj1, addr_obj2])
    addr_grp2, _ = AddressObjectGroup.objects.get_or_create(name="addr group2", status=status)
    addr_grp2.address_objects.set([addr_obj3, addr_obj4])
    addr_grp3, _ = AddressObjectGroup.objects.get_or_create(name="addr group3", status=status)
    addr_grp3.address_objects.set([addr_obj1, addr_obj2, addr_obj3, addr_obj4])
    return addr_grp1, addr_grp2, addr_grp3


def create_svc_obj():
    """Creates 3 of all objects."""
    status = Status.objects.get(name="Active")
    svc_obj1, _ = ServiceObject.objects.get_or_create(name="PGSQL", port="5432", ip_protocol="TCP", status=status)
    svc_obj2, _ = ServiceObject.objects.get_or_create(name="SSH", port="22", ip_protocol="TCP", status=status)
    svc_obj3, _ = ServiceObject.objects.get_or_create(name="DNS", port="53", ip_protocol="TCP", status=status)
    src_svc, _ = ServiceObject.objects.get_or_create(name="Source HTTPS", port="443", ip_protocol="TCP", status=status)
    return svc_obj1, svc_obj2, svc_obj3, src_svc


def create_svc_group():
    """Creates 3 of all objects."""
    svc_obj1, svc_obj2, svc_obj3, _ = create_svc_obj()
    status = Status.objects.get(name="Active")
    svc_grp1, _ = ServiceObjectGroup.objects.get_or_create(name="svc group1", status=status)
    svc_grp1.service_objects.set([svc_obj1])
    svc_grp2, _ = ServiceObjectGroup.objects.get_or_create(name="svc group2", status=status)
    svc_grp2.service_objects.set([svc_obj2, svc_obj3])
    svc_grp3, _ = ServiceObjectGroup.objects.get_or_create(name="svc group3", status=status)
    svc_grp3.service_objects.set([svc_obj1, svc_obj2, svc_obj3])
    return svc_grp1, svc_grp2, svc_grp3


def create_user_obj():
    """Creates 3 of all objects."""
    status = Status.objects.get(name="Active")
    usr_obj1, _ = UserObject.objects.get_or_create(username="user1", name="Bob", status=status)
    usr_obj2, _ = UserObject.objects.get_or_create(username="user2", name="Fred", status=status)
    usr_obj3, _ = UserObject.objects.get_or_create(username="user3", name="Tom", status=status)
    return usr_obj1, usr_obj2, usr_obj3


def create_user_group():
    """Creates 3 of all objects."""
    status = Status.objects.get(name="Active")
    usr_obj1, usr_obj2, usr_obj3 = create_user_obj()
    usr_grp1, _ = UserObjectGroup.objects.get_or_create(name="usr group1", status=status)
    usr_grp1.user_objects.set([usr_obj1])
    usr_grp2, _ = UserObjectGroup.objects.get_or_create(name="usr group2", status=status)
    usr_grp2.user_objects.set([usr_obj1, usr_obj2])
    usr_grp3, _ = UserObjectGroup.objects.get_or_create(name="usr group3", status=status)
    usr_grp3.user_objects.set([usr_obj1, usr_obj2, usr_obj3])
    return usr_grp1, usr_grp2, usr_grp3


def create_zone():
    """Creates 3 of all objects."""
    status = Status.objects.get(name="Active")
    vrf, _ = VRF.objects.get_or_create(name="global")
    zone1, _ = Zone.objects.get_or_create(name="WAN", status=status)
    zone1.vrfs.set([vrf])
    zone2, _ = Zone.objects.get_or_create(name="LAN", status=status)
    zone3, _ = Zone.objects.get_or_create(name="DMZ", status=status)
    return zone1, zone2, zone3


def create_app_obj():
    """Creates 3 of all objects."""
    status = Status.objects.get(name="Active")
    app1, _ = ApplicationObject.objects.get_or_create(
        name="app1",
        category="web",
        subcategory="streaming",
        default_type="443",
        default_ip_protocol="TCP",
        status=status,
        risk=3,
        description="some description",
    )
    app2, _ = ApplicationObject.objects.get_or_create(
        name="app2",
        category="web",
        subcategory="streaming",
        default_type="443",
        default_ip_protocol="TCP",
        status=status,
        risk=2,
        description="some description",
    )
    app3, _ = ApplicationObject.objects.get_or_create(
        name="app3",
        category="web",
        subcategory="streaming",
        default_type="443",
        default_ip_protocol="TCP",
        status=status,
        risk=1,
        description="some description",
    )
    return app1, app2, app3


def create_app_group():
    """Creates 3 of all objects."""
    app1, app2, app3 = create_app_obj()
    status = Status.objects.get(name="Active")
    app_grp1, _ = ApplicationObjectGroup.objects.get_or_create(
        name="streaming", description="some description", status=status
    )
    app_grp1.application_objects.set([app1])
    app_grp2, _ = ApplicationObjectGroup.objects.get_or_create(
        name="gaming", description="some description", status=status
    )
    app_grp2.application_objects.set([app3, app2])
    app_grp3, _ = ApplicationObjectGroup.objects.get_or_create(
        name="news", description="some description", status=status
    )
    app_grp3.application_objects.set([app1, app2, app3])
    return app_grp1, app_grp2, app_grp3


def create_policy_rule():  # pylint: disable=too-many-locals
    """Creates 3 of all objects."""
    app1, app2, app3 = create_app_obj()
    app_grp1, app_grp2, app_grp3 = create_app_group()
    usr_obj1, usr_obj2, usr_obj3 = create_user_obj()
    usr_grp1, usr_grp2, usr_grp3 = create_user_group()
    svc_obj1, svc_obj2, svc_obj3, src_svc = create_svc_obj()
    svc_grp1, svc_grp2, svc_grp3 = create_svc_group()
    zone1, zone2, _ = create_zone()
    addr_obj1, addr_obj2, addr_obj3, addr_obj4 = create_addr_obj()
    addr_grp1, addr_grp2, addr_grp3 = create_addr_group()
    status = Status.objects.get(name="Active")
    pol_rule1, _ = PolicyRule.objects.get_or_create(
        action="deny",
        log=True,
        name="Policy Rule 1",
        status=status,
        request_id="req1",
        index=10,
        description="some description",
    )
    pol_rule1.source_users.set([usr_obj1])
    pol_rule1.source_user_groups.set([usr_grp1])
    pol_rule1.source_addresses.set([addr_obj1])
    pol_rule1.source_address_groups.set([addr_grp1])
    pol_rule1.source_services.set([src_svc])
    pol_rule1.destination_addresses.set([addr_obj4])
    pol_rule1.destination_address_groups.set([addr_grp3])
    pol_rule1.destination_services.set([svc_obj1])
    pol_rule1.destination_service_groups.set([svc_grp1])
    pol_rule1.applications.set([app1])
    pol_rule1.application_groups.set([app_grp1])
    pol_rule2, _ = PolicyRule.objects.get_or_create(
        source_zone=zone1,
        destination_zone=zone2,
        action="allow",
        log=True,
        name="Policy Rule 2",
        status=status,
        request_id="req2",
        index=20,
        description="some description",
    )
    pol_rule2.source_users.set([usr_obj1, usr_obj2])
    pol_rule2.source_user_groups.set([usr_grp1, usr_grp2])
    pol_rule2.source_addresses.set([addr_obj1, addr_obj2])
    pol_rule2.source_address_groups.set([addr_grp1, addr_grp2])
    pol_rule2.destination_addresses.set([addr_obj4])
    pol_rule2.destination_address_groups.set([addr_grp3])
    pol_rule2.destination_services.set([svc_obj1, svc_obj2])
    pol_rule2.destination_service_groups.set([svc_grp1, svc_grp2])
    pol_rule2.applications.set([app2])
    pol_rule2.application_groups.set([app_grp2])
    pol_rule3, _ = PolicyRule.objects.get_or_create(
        source_zone=zone1,
        destination_zone=zone2,
        action="drop",
        log=True,
        name="Policy Rule 3",
        status=status,
        request_id="req3",
        index=30,
        description="some description",
    )
    pol_rule3.source_users.set([usr_obj1, usr_obj2, usr_obj3])
    pol_rule3.source_user_groups.set([usr_grp1, usr_grp2, usr_grp3])
    pol_rule3.source_addresses.set([addr_obj1, addr_obj2, addr_obj3])
    pol_rule3.source_address_groups.set([addr_grp1, addr_grp2])
    pol_rule3.destination_addresses.set([addr_obj4])
    pol_rule3.destination_address_groups.set([addr_grp3])
    pol_rule3.destination_services.set([svc_obj1, svc_obj2, svc_obj3])
    pol_rule3.destination_service_groups.set([svc_grp1, svc_grp2, svc_grp3])
    pol_rule3.applications.set([app2, app3])
    pol_rule3.application_groups.set([app_grp1, app_grp2, app_grp3])
    pol_rule4, _ = PolicyRule.objects.get_or_create(
        name="END OF ACCESS LIST", action="remark", log=False, request_id="req4", index=99
    )
    pol_rule5, _ = PolicyRule.objects.get_or_create(
        name="DENY ALL", action="deny", log=False, request_id="req5", index=100
    )
    return pol_rule1, pol_rule2, pol_rule3, pol_rule4, pol_rule5


def create_policy():
    """Creates 3 of all objects."""
    pol_rule1, pol_rule2, pol_rule3, pol_rule4, pol_rule5 = create_policy_rule()
    status = Status.objects.get(name="Active")
    tenant_group, _ = TenantGroup.objects.get_or_create(name="ABC Holding Corp")
    tenant1, _ = Tenant.objects.get_or_create(name="ABC LLC", tenant_group=tenant_group)
    tenant2, _ = Tenant.objects.get_or_create(name="XYZ LLC")
    pol1, _ = Policy.objects.get_or_create(name="Policy 1", status=status)
    pol1.policy_rules.set([pol_rule1])
    pol2, _ = Policy.objects.get_or_create(name="Policy 2", status=status, tenant=tenant2)
    pol2.policy_rules.set([pol_rule1, pol_rule2])
    pol3, _ = Policy.objects.get_or_create(name="Policy 3", status=status, tenant=tenant1)
    pol3.policy_rules.set([pol_rule1, pol_rule2, pol_rule3, pol_rule4, pol_rule5])
    return pol1, pol2, pol3


def create_natpolicy_rule():  # pylint: disable=too-many-locals
    """Creates 3 of all objects."""
    status = Status.objects.get(name="Active")
    namespace, _ = Namespace.objects.get_or_create(name="global")
    addr_obj1, addr_obj2, addr_obj3, addr_obj4 = create_addr_obj()
    # Nat policies
    nat_orig_dest_service, _ = ServiceObject.objects.get_or_create(
        name="HTTP", port="80", ip_protocol="TCP", status=status
    )
    nat_trans_dest_service, _ = ServiceObject.objects.get_or_create(
        name="HTTP (alt)", port="8080", ip_protocol="TCP", status=status
    )
    original_source_prefix, _ = Prefix.objects.get_or_create(
        network="10.100.0.0", prefix_length=24, status=status, namespace=namespace
    )
    original_source, _ = AddressObject.objects.get_or_create(name="nat-original-source", prefix=original_source_prefix)
    translated_source_prefix, _ = Prefix.objects.get_or_create(
        network="10.200.0.0", prefix_length=24, status=status, namespace=namespace
    )
    translated_source, _ = AddressObject.objects.get_or_create(
        name="nat-translated-source", prefix=translated_source_prefix
    )
    destination_prefix, _ = Prefix.objects.get_or_create(
        network="192.168.0.0", prefix_length=24, status=status, namespace=namespace
    )
    destination, _ = AddressObject.objects.get_or_create(name="nat-destination", prefix=destination_prefix)
    nat_policy_rule_1_1, _ = NATPolicyRule.objects.get_or_create(
        name="NAT Policy Rule 1.1", log=True, request_id="req1"
    )
    nat_policy_rule_1_1.original_source_addresses.add(original_source)
    nat_policy_rule_1_1.translated_source_addresses.add(translated_source)
    nat_policy_rule_1_1.original_destination_addresses.add(destination)
    nat_policy_rule_1_1.translated_destination_addresses.add(destination)
    nat_policy_rule_1_1.original_destination_services.add(nat_orig_dest_service)
    nat_policy_rule_1_1.translated_destination_services.add(nat_trans_dest_service)

    nat_policy_rule_1_2, _ = NATPolicyRule.objects.get_or_create(
        name="END OF NAT POLICY", request_id="req2", remark=True, log=True
    )

    nat_policy_rule_2_1, _ = NATPolicyRule.objects.get_or_create(
        name="NAT Policy Rule 2.1", log=True, request_id="req3"
    )
    nat_policy_rule_2_1.original_source_addresses.set([addr_obj1, addr_obj2])
    nat_policy_rule_2_1.translated_source_addresses.add(translated_source)
    nat_policy_rule_2_1.original_destination_addresses.add(destination)
    nat_policy_rule_2_1.original_destination_services.add(nat_orig_dest_service)

    nat_policy_rule_3_1, _ = NATPolicyRule.objects.get_or_create(
        name="NAT Policy Rule 3.1", log=True, request_id="req4"
    )
    nat_policy_rule_3_1.original_source_addresses.set([addr_obj3, addr_obj4])
    nat_policy_rule_3_1.translated_source_addresses.add(translated_source)
    nat_policy_rule_3_1.original_destination_addresses.add(destination)
    nat_policy_rule_3_1.original_destination_services.add(nat_orig_dest_service)
    return nat_policy_rule_1_1, nat_policy_rule_1_2, nat_policy_rule_2_1, nat_policy_rule_3_1


def create_natpolicy():
    """Creates 3 of all objects."""
    nat_policy_rule_1_1, nat_policy_rule_1_2, nat_policy_rule_2_1, nat_policy_rule_3_1 = create_natpolicy_rule()
    nat_policy_1, _ = NATPolicy.objects.get_or_create(name="NAT Policy 1")
    nat_policy_2, _ = NATPolicy.objects.get_or_create(name="NAT Policy 2")
    nat_policy_3, _ = NATPolicy.objects.get_or_create(name="NAT Policy 3")
    nat_policy_1.nat_policy_rules.add(nat_policy_rule_1_1)
    nat_policy_1.nat_policy_rules.add(nat_policy_rule_1_2)
    nat_policy_2.nat_policy_rules.add(nat_policy_rule_2_1)
    nat_policy_2.nat_policy_rules.add(nat_policy_rule_3_1)
    return nat_policy_1, nat_policy_2, nat_policy_3


def assign_policies():  # pylint: disable=too-many-locals
    """Creates 3 of all objects."""
    status = Status.objects.get(name="Active")
    nat_policy_1, nat_policy_2, nat_policy_3 = create_natpolicy()
    pol1, pol2, pol3 = create_policy()
    # Mapping policies to devices
    loc_type, _ = LocationType.objects.get_or_create(name="site")
    site1, _ = Location.objects.get_or_create(name="DFW02", location_type=loc_type, status=status)
    site2, _ = Location.objects.get_or_create(name="HOU02", location_type=loc_type, status=status)
    jun_manufacturer, _ = Manufacturer.objects.get_or_create(name="Juniper")
    jun_platform, _ = Platform.objects.get_or_create(name="Juniper", network_driver="srx")
    jun_dev_type, _ = DeviceType.objects.get_or_create(manufacturer=jun_manufacturer, model="SRX300")
    palo_manufacturer, _ = Manufacturer.objects.get_or_create(name="Palo Alto")
    palo_platform, _ = Platform.objects.get_or_create(name="Palo Alto", network_driver="paloalto")
    palo_dev_type, _ = DeviceType.objects.get_or_create(manufacturer=palo_manufacturer, model="PA-3020")
    dev_role, _ = Role.objects.get_or_create(name="WAN")
    dev_role.content_types.add(ContentType.objects.get_for_model(Device))
    dev1, _ = Device.objects.get_or_create(
        name="DFW02-WAN00",
        role=dev_role,
        device_type=jun_dev_type,
        location=site1,
        status=status,
        platform=jun_platform,
    )
    Device.objects.get_or_create(
        name="DFW02-WAN01",
        role=dev_role,
        device_type=jun_dev_type,
        location=site1,
        status=status,
        platform=jun_platform,
    )
    dev2, _ = Device.objects.get_or_create(
        name="HOU02-WAN00",
        role=dev_role,
        device_type=palo_dev_type,
        location=site2,
        status=status,
        platform=palo_platform,
    )
    dynamic_group, _ = DynamicGroup.objects.get_or_create(
        name="North Texas", content_type=ContentType.objects.get_for_model(Device)
    )
    dynamic_group.filter = {"location": ["DFW02"]}
    dynamic_group.validated_save()
    PolicyDeviceM2M.objects.get_or_create(policy=pol1, device=dev1, weight=150)
    PolicyDeviceM2M.objects.get_or_create(policy=pol2, device=dev1, weight=200)
    PolicyDeviceM2M.objects.get_or_create(policy=pol1, device=dev2)
    PolicyDynamicGroupM2M.objects.get_or_create(policy=pol3, dynamic_group=dynamic_group, weight=1000)
    NATPolicyDeviceM2M.objects.get_or_create(nat_policy=nat_policy_1, device=dev1, weight=150)
    NATPolicyDeviceM2M.objects.get_or_create(nat_policy=nat_policy_2, device=dev1, weight=200)
    NATPolicyDeviceM2M.objects.get_or_create(nat_policy=nat_policy_1, device=dev2)
    NATPolicyDynamicGroupM2M.objects.get_or_create(nat_policy=nat_policy_3, dynamic_group=dynamic_group, weight=1000)


def create_capirca_env():
    """Create objects that are Capirca Ready."""  # pylint: disable=too-many-locals, too-many-statements
    assign_policies()
    namespace, _ = Namespace.objects.get_or_create(name="global")
    status = Status.objects.get(name="Active")
    zoneall, _ = Zone.objects.get_or_create(name="all", status=status)

    pol_rule1 = PolicyRule.objects.get(name="Policy Rule 1")
    pol_rule1.source_zone = Zone.objects.get(name="DMZ")
    pol_rule1.destination_zone = Zone.objects.get(name="WAN")
    pol_rule1.validated_save()

    pol_rule4 = PolicyRule.objects.get(name="END OF ACCESS LIST")
    pol_rule4.source_zone = zoneall
    pol_rule4.destination_zone = zoneall
    pol_rule4.validated_save()

    pol_rule5 = PolicyRule.objects.get(name="DENY ALL")
    pol_rule5.source_zone = zoneall
    pol_rule5.destination_zone = zoneall
    pol_rule5.validated_save()

    ip_address, _ = IPAddr.objects.get_or_create(
        address="10.0.0.100", status=status, parent=Prefix.objects.get(network="10.0.0.0", namespace=namespace)
    )
    prefix, _ = Prefix.objects.get_or_create(network="10.1.0.0", prefix_length=24, status=status, namespace=namespace)

    addr_obj1 = AddressObject.objects.get(name="printer")
    addr_obj1.ip_range = None
    addr_obj1.ip_address = ip_address
    addr_obj1.validated_save()

    addr_obj4 = AddressObject.objects.get(name="server")
    addr_obj4.fqdn = None
    addr_obj4.prefix = prefix
    addr_obj4.validated_save()

    job = Job.objects.get(name="Generate FW Config via Capirca.")
    job.enabled = True
    job.validated_save()
