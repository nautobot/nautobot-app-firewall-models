"""Create basic objects for use in test class setup."""
# flake8: noqa: F403,405
from django.contrib.contenttypes.models import ContentType
from nautobot.dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site
from nautobot.extras.models import DynamicGroup
from nautobot.extras.models.statuses import Status
from nautobot.ipam.models import Prefix, VRF
from nautobot.ipam.models import IPAddress as IPAddr

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
    addr_obj1 = AddressObject.objects.create(name="data", ip_range=ip_range, status=status)
    addr_obj2 = AddressObject.objects.create(name="voice", ip_address=ip_address, status=status)
    addr_obj3 = AddressObject.objects.create(name="storage", prefix=prefix, status=status)
    addr_obj4 = AddressObject.objects.create(name="server", fqdn=fqdn, status=status)
    addr_grp1 = AddressObjectGroup.objects.create(name="group1", status=status)
    addr_grp1.address_objects.set([addr_obj1, addr_obj2])
    addr_grp2 = AddressObjectGroup.objects.create(name="group2", status=status)
    addr_grp2.address_objects.set([addr_obj3, addr_obj4])
    addr_grp3 = AddressObjectGroup.objects.create(name="group3", status=status)
    addr_grp3.address_objects.set([addr_obj1, addr_obj2, addr_obj3, addr_obj4])

    svc_obj1, _ = ServiceObject.objects.get_or_create(name="PGSQL", port="5432", ip_protocol="TCP", status=status)
    svc_obj2, _ = ServiceObject.objects.get_or_create(name="SSH", port="22", ip_protocol="TCP", status=status)
    svc_obj3, _ = ServiceObject.objects.get_or_create(name="FTP", port="20-21", ip_protocol="TCP", status=status)
    svc_grp1 = ServiceObjectGroup.objects.create(name="group1", status=status)
    svc_grp1.service_objects.set([svc_obj1])
    svc_grp2 = ServiceObjectGroup.objects.create(name="group2", status=status)
    svc_grp2.service_objects.set([svc_obj2, svc_obj3])
    svc_grp3 = ServiceObjectGroup.objects.create(name="group3", status=status)
    svc_grp3.service_objects.set([svc_obj1, svc_obj2, svc_obj3])
    usr_obj1 = UserObject.objects.create(username="user1", name="User 1", status=status)
    usr_obj2 = UserObject.objects.create(username="user2", name="User 2", status=status)
    usr_obj3 = UserObject.objects.create(username="user3", name="User 3", status=status)
    usr_grp1 = UserObjectGroup.objects.create(name="group1", status=status)
    usr_grp1.user_objects.set([usr_obj1])
    usr_grp2 = UserObjectGroup.objects.create(name="group2", status=status)
    usr_grp2.user_objects.set([usr_obj1, usr_obj2])
    usr_grp3 = UserObjectGroup.objects.create(name="group3", status=status)
    usr_grp3.user_objects.set([usr_obj1, usr_obj2, usr_obj3])

    zone1 = Zone.objects.create(name="WAN", status=status)
    zone1.vrfs.set([vrf])
    zone2 = Zone.objects.create(name="LAN", status=status)
    Zone.objects.create(name="DMZ", status=status)

    pol_rule1 = PolicyRule.objects.create(
        action="Deny",
        log=True,
        name="Policy Rule 1",
        status=status,
    )
    pol_rule1.source_user.set([usr_obj1])
    pol_rule1.source_user_group.set([usr_grp1])
    pol_rule1.source_address.set([addr_obj1])
    pol_rule1.source_address_group.set([addr_grp1])
    pol_rule1.destination_address.set([addr_obj4])
    pol_rule1.destination_address_group.set([addr_grp3])
    pol_rule1.service.set([svc_obj1])
    pol_rule1.service_group.set([svc_grp1])
    pol_rule2 = PolicyRule.objects.create(
        source_zone=zone1,
        destination_zone=zone2,
        action="Allow",
        log=True,
        name="Policy Rule 2",
        status=status,
    )
    pol_rule2.source_user.set([usr_obj1, usr_obj2])
    pol_rule2.source_user_group.set([usr_grp1, usr_grp2])
    pol_rule2.source_address.set([addr_obj1, addr_obj2])
    pol_rule2.source_address_group.set([addr_grp1, addr_grp2])
    pol_rule2.destination_address.set([addr_obj4])
    pol_rule2.destination_address_group.set([addr_grp3])
    pol_rule2.service.set([svc_obj1, svc_obj2])
    pol_rule2.service_group.set([svc_grp1, svc_grp2])
    pol_rule3 = PolicyRule.objects.create(
        source_zone=zone1,
        destination_zone=zone2,
        action="Drop",
        log=True,
        name="Policy Rule 3",
        status=status,
    )
    pol_rule3.source_user.set([usr_obj1, usr_obj2, usr_obj3])
    pol_rule3.source_user_group.set([usr_grp1, usr_grp2, usr_grp3])
    pol_rule3.source_address.set([addr_obj1, addr_obj2, addr_obj3])
    pol_rule3.source_address_group.set([addr_grp1, addr_grp2])
    pol_rule3.destination_address.set([addr_obj4])
    pol_rule3.destination_address_group.set([addr_grp3])
    pol_rule3.service.set([svc_obj1, svc_obj2, svc_obj3])
    pol_rule3.service_group.set([svc_grp1, svc_grp2, svc_grp3])
    pol1 = Policy.objects.create(name="Policy 1", status=status)
    pol1.policy_rules.set([pol_rule1])
    pol2 = Policy.objects.create(name="Policy 2", status=status)
    PolicyRuleM2M.objects.create(policy=pol2, rule=pol_rule1, index=10)
    PolicyRuleM2M.objects.create(policy=pol2, rule=pol_rule2, index=20)
    pol3 = Policy.objects.create(name="Policy 3", status=status)
    PolicyRuleM2M.objects.create(policy=pol3, rule=pol_rule1, index=10)
    PolicyRuleM2M.objects.create(policy=pol3, rule=pol_rule2, index=20)
    PolicyRuleM2M.objects.create(policy=pol3, rule=pol_rule3)
    site1 = Site.objects.create(name="DFW", slug="dfw")
    site2 = Site.objects.create(name="HOU", slug="hou")
    manufacturer = Manufacturer.objects.create(name="Juniper", slug="juniper")
    dev_type = DeviceType.objects.create(manufacturer=manufacturer, model="SRX300", slug="srx300")
    dev_role = DeviceRole.objects.create(name="WAN", slug="wan")
    dev1 = Device.objects.create(
        name="DFW-WAN00", device_role=dev_role, device_type=dev_type, site=site1, status=status
    )
    dev2 = Device.objects.create(
        name="HOU-WAN00", device_role=dev_role, device_type=dev_type, site=site2, status=status
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
