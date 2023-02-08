"""Create basic objects for use in test class setup."""
# flake8: noqa: F403,405
from django.contrib.contenttypes.models import ContentType
from nautobot.dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Platform, Site
from nautobot.extras.models import DynamicGroup, Job
from nautobot.extras.models.statuses import Status
from nautobot.ipam.models import Prefix, VRF
from nautobot.ipam.models import IPAddress as IPAddr
from nautobot.tenancy.models import Tenant, TenantGroup

from nautobot_firewall_models.models import *  # pylint: disable=unused-wildcard-import, wildcard-import


def create_ip_range():
    """Creates 3 IPRange objects."""
    status = Status.objects.get(slug="active")
    vrf = VRF.objects.create(name="global")
    IPRange.objects.create(start_address="192.168.0.1", end_address="192.168.0.10", status=status)
    IPRange.objects.create(start_address="192.168.0.1", end_address="192.168.0.10", vrf=vrf, status=status)
    return IPRange.objects.create(start_address="192.168.0.11", end_address="192.168.0.20", status=status)


def create_fqdn():
    """Creates 3 FQDN objects."""
    status = Status.objects.get(slug="active")
    FQDN.objects.create(name="test.dev", status=status)
    FQDN.objects.create(name="test.uat", status=status)
    return FQDN.objects.create(name="test.prod", status=status)


def create_env():
    """Creates 3 of all objects."""  # pylint: disable=too-many-locals, too-many-statements
    # Core Models
    vrf = VRF.objects.create(name="global")
    ip_address = IPAddr.objects.create(address="10.0.0.1")
    prefix = Prefix.objects.create(network="10.0.0.0", prefix_length=24)
    status = Status.objects.get(slug="active")

    # Plugin Models
    ip_range = create_ip_range()
    fqdn = create_fqdn()
    addr_obj1 = AddressObject.objects.create(name="printer", ip_range=ip_range, status=status)
    addr_obj2 = AddressObject.objects.create(name="voice", ip_address=ip_address, status=status)
    addr_obj3 = AddressObject.objects.create(name="storage", prefix=prefix, status=status)
    addr_obj4 = AddressObject.objects.create(name="server", fqdn=fqdn, status=status)
    addr_grp1 = AddressObjectGroup.objects.create(name="addr group1", status=status)
    addr_grp1.address_objects.set([addr_obj1, addr_obj2])
    addr_grp2 = AddressObjectGroup.objects.create(name="addr group2", status=status)
    addr_grp2.address_objects.set([addr_obj3, addr_obj4])
    addr_grp3 = AddressObjectGroup.objects.create(name="addr group3", status=status)
    addr_grp3.address_objects.set([addr_obj1, addr_obj2, addr_obj3, addr_obj4])

    svc_obj1, _ = ServiceObject.objects.get_or_create(name="PGSQL", port="5432", ip_protocol="TCP", status=status)
    svc_obj2, _ = ServiceObject.objects.get_or_create(name="SSH", port="22", ip_protocol="TCP", status=status)
    svc_obj3, _ = ServiceObject.objects.get_or_create(name="DNS", port="53", ip_protocol="TCP", status=status)
    src_svc, _ = ServiceObject.objects.get_or_create(name="Source HTTPS", port="443", ip_protocol="TCP", status=status)
    svc_grp1 = ServiceObjectGroup.objects.create(name="svc group1", status=status)
    svc_grp1.service_objects.set([svc_obj1])
    svc_grp2 = ServiceObjectGroup.objects.create(name="svc group2", status=status)
    svc_grp2.service_objects.set([svc_obj2, svc_obj3])
    svc_grp3 = ServiceObjectGroup.objects.create(name="svc group3", status=status)
    svc_grp3.service_objects.set([svc_obj1, svc_obj2, svc_obj3])
    usr_obj1 = UserObject.objects.create(username="user1", name="User 1", status=status)
    usr_obj2 = UserObject.objects.create(username="user2", name="User 2", status=status)
    usr_obj3 = UserObject.objects.create(username="user3", name="User 3", status=status)
    usr_grp1 = UserObjectGroup.objects.create(name="usr group1", status=status)
    usr_grp1.user_objects.set([usr_obj1])
    usr_grp2 = UserObjectGroup.objects.create(name="usr group2", status=status)
    usr_grp2.user_objects.set([usr_obj1, usr_obj2])
    usr_grp3 = UserObjectGroup.objects.create(name="usr group3", status=status)
    usr_grp3.user_objects.set([usr_obj1, usr_obj2, usr_obj3])

    zone1 = Zone.objects.create(name="WAN", status=status)
    zone1.vrfs.set([vrf])
    zone2 = Zone.objects.create(name="LAN", status=status)
    Zone.objects.create(name="DMZ", status=status)

    app1 = ApplicationObject.objects.create(
        name="app1",
        category="web",
        subcategory="streaming",
        default_type="443",
        default_ip_protocol="TCP",
        status=status,
        risk=3,
        description="some description",
    )
    app2 = ApplicationObject.objects.create(
        name="app2",
        category="web",
        subcategory="streaming",
        default_type="443",
        default_ip_protocol="TCP",
        status=status,
        risk=2,
        description="some description",
    )
    app3 = ApplicationObject.objects.create(
        name="app3",
        category="web",
        subcategory="streaming",
        default_type="443",
        default_ip_protocol="TCP",
        status=status,
        risk=1,
        description="some description",
    )
    app_grp1 = ApplicationObjectGroup.objects.create(name="streaming", description="some description")
    app_grp1.application_objects.set([app1])
    app_grp2 = ApplicationObjectGroup.objects.create(name="gaming", description="some description")
    app_grp2.application_objects.set([app3, app2])
    app_grp3 = ApplicationObjectGroup.objects.create(name="news", description="some description")
    app_grp3.application_objects.set([app1, app2, app3])

    pol_rule1 = PolicyRule.objects.create(
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
    pol_rule2 = PolicyRule.objects.create(
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
    pol_rule3 = PolicyRule.objects.create(
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
    pol_rule4 = PolicyRule.objects.create(
        name="END OF ACCESS LIST", action="remark", log=False, request_id="req4", index=99
    )
    pol_rule5 = PolicyRule.objects.create(name="DENY ALL", action="deny", log=False, request_id="req5", index=100)
    tenant_group = TenantGroup.objects.create(name="ABC Holding Corp", slug="abc-holding-corp")
    tenant1 = Tenant.objects.create(name="ABC LLC", slug="abc-llc", group=tenant_group)
    tenant2 = Tenant.objects.create(name="XYZ LLC", slug="xyz-llc")
    pol1 = Policy.objects.create(name="Policy 1", status=status)
    pol1.policy_rules.set([pol_rule1])
    pol2 = Policy.objects.create(name="Policy 2", status=status, tenant=tenant2)
    PolicyRuleM2M.objects.create(policy=pol2, rule=pol_rule1)
    PolicyRuleM2M.objects.create(policy=pol2, rule=pol_rule2)
    pol3 = Policy.objects.create(name="Policy 3", status=status, tenant=tenant1)
    PolicyRuleM2M.objects.create(policy=pol3, rule=pol_rule1)
    PolicyRuleM2M.objects.create(policy=pol3, rule=pol_rule2)
    PolicyRuleM2M.objects.create(policy=pol3, rule=pol_rule3)
    PolicyRuleM2M.objects.create(policy=pol3, rule=pol_rule4)
    PolicyRuleM2M.objects.create(policy=pol3, rule=pol_rule5)

    # Nat policies
    nat_orig_dest_service, _ = ServiceObject.objects.get_or_create(
        name="HTTP", port="80", ip_protocol="TCP", status=status
    )
    nat_trans_dest_service, _ = ServiceObject.objects.get_or_create(
        name="HTTP (alt)", port="8080", ip_protocol="TCP", status=status
    )
    original_source_prefix = Prefix.objects.create(network="10.100.0.0", prefix_length=24)
    original_source = AddressObject.objects.create(name="nat-original-source", prefix=original_source_prefix)
    translated_source_prefix = Prefix.objects.create(network="10.200.0.0", prefix_length=24)
    translated_source = AddressObject.objects.create(name="nat-translated-source", prefix=translated_source_prefix)
    destination_prefix = Prefix.objects.create(network="192.168.0.0", prefix_length=24)
    destination = AddressObject.objects.create(name="nat-destination", prefix=destination_prefix)

    nat_policy_1 = NATPolicy.objects.create(name="NAT Policy 1")
    nat_policy_2 = NATPolicy.objects.create(name="NAT Policy 2")
    nat_policy_3 = NATPolicy.objects.create(name="NAT Policy 3")
    nat_policy_rule_1_1 = NATPolicyRule.objects.create(name="NAT Policy Rule 1.1", log=True, request_id="req1")
    nat_policy_rule_1_1.original_source_addresses.add(original_source)
    nat_policy_rule_1_1.translated_source_addresses.add(translated_source)
    nat_policy_rule_1_1.original_destination_addresses.add(destination)
    nat_policy_rule_1_1.translated_destination_addresses.add(destination)
    nat_policy_rule_1_1.original_destination_services.add(nat_orig_dest_service)
    nat_policy_rule_1_1.translated_destination_services.add(nat_trans_dest_service)
    nat_policy_1.nat_policy_rules.add(nat_policy_rule_1_1)

    nat_policy_rule_1_2 = NATPolicyRule.objects.create(
        name="END OF NAT POLICY",
        request_id="req2",
        remark=True,
    )
    nat_policy_1.nat_policy_rules.add(nat_policy_rule_1_2)

    nat_policy_rule_2_1 = NATPolicyRule.objects.create(name="NAT Policy Rule 2.1", log=True, request_id="req3")
    nat_policy_rule_2_1.original_source_addresses.add(addr_obj1)
    nat_policy_rule_2_1.translated_source_addresses.add(translated_source)
    nat_policy_rule_2_1.original_destination_addresses.add(destination)
    nat_policy_rule_2_1.original_destination_services.add(nat_orig_dest_service)
    nat_policy_2.nat_policy_rules.add(nat_policy_rule_2_1)

    # Mapping policies to devices
    site1 = Site.objects.create(name="DFW", slug="dfw")
    site2 = Site.objects.create(name="HOU", slug="hou")
    jun_manufacturer = Manufacturer.objects.create(name="Juniper", slug="juniper")
    jun_platform = Platform.objects.create(name="Juniper", slug="srx")
    jun_dev_type = DeviceType.objects.create(manufacturer=jun_manufacturer, model="SRX300", slug="srx300")
    palo_manufacturer = Manufacturer.objects.create(name="Palo Alto", slug="paloalto")
    palo_platform = Platform.objects.create(name="Palo Alto", slug="paloalto")
    palo_dev_type = DeviceType.objects.create(manufacturer=palo_manufacturer, model="PA-3020", slug="pa3020")
    dev_role = DeviceRole.objects.create(name="WAN", slug="wan")
    dev1 = Device.objects.create(
        name="DFW-WAN00",
        device_role=dev_role,
        device_type=jun_dev_type,
        site=site1,
        status=status,
        platform=jun_platform,
    )
    dev2 = Device.objects.create(
        name="HOU-WAN00",
        device_role=dev_role,
        device_type=palo_dev_type,
        site=site2,
        status=status,
        platform=palo_platform,
    )
    dynamic_group = DynamicGroup.objects.create(
        name="North Texas", slug="north-texas", content_type=ContentType.objects.get_for_model(Device)
    )
    dynamic_group.filter = {"site": ["dfw"]}
    dynamic_group.save()
    PolicyDeviceM2M.objects.create(policy=pol1, device=dev1, weight=150)
    PolicyDeviceM2M.objects.create(policy=pol2, device=dev1, weight=200)
    PolicyDeviceM2M.objects.create(policy=pol1, device=dev2)
    PolicyDynamicGroupM2M.objects.create(policy=pol3, dynamic_group=dynamic_group, weight=1000)
    NATPolicyDeviceM2M.objects.create(nat_policy=nat_policy_1, device=dev1, weight=150)
    NATPolicyDeviceM2M.objects.create(nat_policy=nat_policy_2, device=dev1, weight=200)
    NATPolicyDeviceM2M.objects.create(nat_policy=nat_policy_1, device=dev2)
    NATPolicyDynamicGroupM2M.objects.create(nat_policy=nat_policy_3, dynamic_group=dynamic_group, weight=1000)


def create_capirca_env():
    """Create objects that are Capirca Ready."""  # pylint: disable=too-many-locals, too-many-statements
    create_env()
    status = Status.objects.get(slug="active")
    zoneall = Zone.objects.create(name="all", status=status)

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

    ip_address = IPAddr.objects.create(address="10.0.0.100")
    prefix = Prefix.objects.create(network="10.1.0.0", prefix_length=24)

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
