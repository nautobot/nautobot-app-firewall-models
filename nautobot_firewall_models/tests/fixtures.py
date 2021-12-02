"""Create basic objects for use in test class setup."""
# flake8: noqa: F403,405
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


def create_role():
    """Creates 3 Role objects."""
    Role.objects.create(name="DEV", slug="dev")
    Role.objects.create(name="UAT", slug="uat")
    return Role.objects.create(name="PROD", slug="prod")


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
    role = create_role()
    addr_obj1 = AddressObject.objects.create(name="data", ip_range=ip_range, status=status, role=role)
    addr_obj2 = AddressObject.objects.create(name="voice", ip_address=ip_address, status=status)
    addr_obj3 = AddressObject.objects.create(name="storage", prefix=prefix, status=status)
    addr_obj4 = AddressObject.objects.create(name="server", fqdn=fqdn, status=status)
    addr_grp1 = AddressObjectGroup.objects.create(name="group1", status=status, role=role)
    addr_grp1.address_objects.set([addr_obj1, addr_obj2])
    addr_grp2 = AddressObjectGroup.objects.create(name="group2", status=status)
    addr_grp2.address_objects.set([addr_obj3, addr_obj4])
    addr_grp3 = AddressObjectGroup.objects.create(name="group3", status=status)
    addr_grp3.address_objects.set([addr_obj1, addr_obj2, addr_obj3, addr_obj4])
    addr_pol1 = AddressPolicyObject.objects.create(name="policy1", status=status, role=role)
    addr_pol1.address_objects.set([addr_obj1, addr_obj2])
    addr_pol2 = AddressPolicyObject.objects.create(name="policy2", status=status)
    addr_pol2.address_object_groups.set([addr_grp2])
    addr_pol3 = AddressPolicyObject.objects.create(name="policy3", status=status)
    addr_pol3.address_objects.set([addr_obj1, addr_obj2])
    addr_pol3.address_object_groups.set([addr_grp2])
    svc_obj1 = ServiceObject.objects.create(name="PGSQL", port=5432, ip_protocol="TCP", status=status, role=role)
    svc_obj2 = ServiceObject.objects.create(name="SSH", port=22, status=status)
    svc_obj3 = ServiceObject.objects.create(name="TELNET", port=23, status=status)
    svc_grp1 = ServiceObjectGroup.objects.create(name="group1", status=status, role=role)
    svc_grp1.service_objects.set([svc_obj1])
    svc_grp2 = ServiceObjectGroup.objects.create(name="group2", status=status)
    svc_grp2.service_objects.set([svc_obj2, svc_obj3])
    svc_grp3 = ServiceObjectGroup.objects.create(name="group3", status=status)
    svc_grp3.service_objects.set([svc_obj1, svc_obj2, svc_obj3])
    svc_pol1 = ServicePolicyObject.objects.create(name="policy1", status=status, role=role)
    svc_pol1.service_objects.set([svc_obj1, svc_obj2])
    svc_pol2 = ServicePolicyObject.objects.create(name="policy2", status=status)
    svc_pol2.service_object_groups.set([svc_grp2])
    svc_pol3 = ServicePolicyObject.objects.create(name="policy3", status=status)
    svc_pol3.service_objects.set([svc_obj1, svc_obj2])
    svc_pol3.service_object_groups.set([svc_grp2])
    usr_obj1 = UserObject.objects.create(username="user1", name="User 1", status=status, role=role)
    usr_obj2 = UserObject.objects.create(username="user2", name="User 2", status=status)
    usr_obj3 = UserObject.objects.create(username="user3", name="User 3", status=status)
    usr_grp1 = UserObjectGroup.objects.create(name="group1", status=status, role=role)
    usr_grp1.user_objects.set([usr_obj1])
    usr_grp2 = UserObjectGroup.objects.create(name="group2", status=status)
    usr_grp2.user_objects.set([usr_obj1, usr_obj2])
    usr_grp3 = UserObjectGroup.objects.create(name="group3", status=status)
    usr_grp3.user_objects.set([usr_obj1, usr_obj2, usr_obj3])
    usr_pol1 = UserPolicyObject.objects.create(name="policy1", status=status, role=role)
    usr_pol1.user_objects.set([usr_obj1, usr_obj2])
    usr_pol2 = UserPolicyObject.objects.create(name="policy2", status=status)
    usr_pol2.user_object_groups.set([usr_grp3])
    usr_pol3 = UserPolicyObject.objects.create(name="policy3", status=status)
    usr_pol3.user_objects.set([usr_obj3])
    usr_pol3.user_object_groups.set([usr_grp2])
    zone = Zone.objects.create(name="WAN", status=status, role=role)
    zone.vrfs.set([vrf])
    Zone.objects.create(name="LAN", status=status)
    Zone.objects.create(name="DMZ", status=status)
    src1 = SourceDestination.objects.create(
        description="test desc", address=addr_pol1, service=svc_pol1, user=usr_pol1, zone=zone, status=status, role=role
    )
    src2 = SourceDestination.objects.create(address=addr_pol1, service=svc_pol1, user=usr_pol1, status=status)
    src3 = SourceDestination.objects.create(address=addr_pol1, service=svc_pol1, zone=zone, status=status)
    dest1 = SourceDestination.objects.create(
        description="test desc", address=addr_pol2, service=svc_pol2, zone=zone, status=status, role=role
    )
    dest2 = SourceDestination.objects.create(address=addr_pol2, service=svc_pol2, status=status)
    dest3 = SourceDestination.objects.create(address=addr_pol3, service=svc_pol3, zone=zone, status=status)
    pol_rule1 = PolicyRule.objects.create(
        source=src1, destination=dest1, action="Deny", log=True, index=1, name="Policy Rule 1", status=status, role=role
    )
    pol_rule2 = PolicyRule.objects.create(
        source=src2, destination=dest2, action="Allow", log=True, index=2, name="Policy Rule 2", status=status
    )
    pol_rule3 = PolicyRule.objects.create(
        source=src3, destination=dest3, action="Drop", log=True, index=3, name="Policy Rule 3", status=status
    )
    pol1 = Policy.objects.create(name="Policy 1", status=status, role=role)
    pol1.policy_rules.set([pol_rule1])
    pol2 = Policy.objects.create(name="Policy 2", status=status)
    pol2.policy_rules.set([pol_rule1, pol_rule2])
    pol3 = Policy.objects.create(name="Policy 3", status=status)
    pol3.policy_rules.set([pol_rule1, pol_rule2, pol_rule3])
