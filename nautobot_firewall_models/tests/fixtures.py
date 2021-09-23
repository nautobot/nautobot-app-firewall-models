"""Create basic objects for use in test class setup."""
# flake8: noqa: F403,405
from nautobot.ipam.models import Prefix, VRF
from nautobot.ipam.models import IPAddress as IPAddr

from nautobot_firewall_models.models import *  # pylint: disable=unused-wildcard-import, wildcard-import


def create_env():
    """Creates 3 of all objects."""  # pylint: disable=too-many-locals, too-many-statements
    # Core Models
    vrf = VRF.objects.create(name="global")
    ip_address = IPAddr.objects.create(address="10.0.0.1")
    prefix = Prefix.objects.create(network="10.0.0.0", prefix_length=24)

    # Plugin Models
    ip_range = IPRange.objects.create(start_address="192.168.0.1", end_address="192.168.0.10")
    IPRange.objects.create(start_address="192.168.0.1", end_address="192.168.0.10", vrf=vrf)
    IPRange.objects.create(start_address="192.168.0.11", end_address="192.168.0.20")
    fqdn = FQDN.objects.create(name="test.dev")
    FQDN.objects.create(name="test.uat")
    FQDN.objects.create(name="test.prod")
    addr_obj1 = AddressObject.objects.create(name="data", ip_range=ip_range)
    addr_obj2 = AddressObject.objects.create(name="voice", ip_address=ip_address)
    addr_obj3 = AddressObject.objects.create(name="storage", prefix=prefix)
    addr_obj4 = AddressObject.objects.create(name="server", fqdn=fqdn)
    addr_grp1 = AddressObjectGroup.objects.create(name="group1")
    addr_grp1.address_objects.set([addr_obj1, addr_obj2])
    addr_grp2 = AddressObjectGroup.objects.create(name="group2")
    addr_grp2.address_objects.set([addr_obj3, addr_obj4])
    addr_grp3 = AddressObjectGroup.objects.create(name="group3")
    addr_grp3.address_objects.set([addr_obj1, addr_obj2, addr_obj3, addr_obj4])
    addr_pol1 = AddressPolicyObject.objects.create(name="policy1")
    addr_pol1.address_objects.set([addr_obj1, addr_obj2])
    addr_pol2 = AddressPolicyObject.objects.create(name="policy2")
    addr_pol2.address_object_groups.set([addr_grp2])
    addr_pol3 = AddressPolicyObject.objects.create(name="policy3")
    addr_pol3.address_objects.set([addr_obj1, addr_obj2])
    addr_pol3.address_object_groups.set([addr_grp2])
    svc_obj1 = ServiceObject.objects.create(name="PGSQL", port=5432, ip_protocol="TCP")
    svc_obj2 = ServiceObject.objects.create(name="SSH", port=22)
    svc_obj3 = ServiceObject.objects.create(name="TELNET", port=23)
    svc_grp1 = ServiceObjectGroup.objects.create(name="group1")
    svc_grp1.service_objects.set([svc_obj1])
    svc_grp2 = ServiceObjectGroup.objects.create(name="group2")
    svc_grp2.service_objects.set([svc_obj2, svc_obj3])
    svc_grp3 = ServiceObjectGroup.objects.create(name="group3")
    svc_grp3.service_objects.set([svc_obj1, svc_obj2, svc_obj3])
    svc_pol1 = ServicePolicyObject.objects.create(name="policy1")
    svc_pol1.service_objects.set([svc_obj1, svc_obj2])
    svc_pol2 = ServicePolicyObject.objects.create(name="policy2")
    svc_pol2.service_object_groups.set([svc_grp2])
    svc_pol3 = ServicePolicyObject.objects.create(name="policy3")
    svc_pol3.service_objects.set([svc_obj1, svc_obj2])
    svc_pol3.service_object_groups.set([svc_grp2])
    usr_obj1 = UserObject.objects.create(username="user1", name="User 1")
    usr_obj2 = UserObject.objects.create(username="user2", name="User 2")
    usr_obj3 = UserObject.objects.create(username="user3", name="User 3")
    usr_grp1 = UserObjectGroup.objects.create(name="group1")
    usr_grp1.user_objects.set([usr_obj1])
    usr_grp2 = UserObjectGroup.objects.create(name="group2")
    usr_grp2.user_objects.set([usr_obj1, usr_obj2])
    usr_grp3 = UserObjectGroup.objects.create(name="group3")
    usr_grp3.user_objects.set([usr_obj1, usr_obj2, usr_obj3])
    usr_pol1 = UserPolicyObject.objects.create(name="policy1")
    usr_pol1.user_objects.set([usr_obj1, usr_obj2])
    usr_pol2 = UserPolicyObject.objects.create(name="policy2")
    usr_pol2.user_object_groups.set([usr_grp3])
    usr_pol3 = UserPolicyObject.objects.create(name="policy3")
    usr_pol3.user_objects.set([usr_obj3])
    usr_pol3.user_object_groups.set([usr_grp2])
    zone = Zone.objects.create(name="WAN")
    zone.vrfs.set([vrf])
    Zone.objects.create(name="LAN")
    Zone.objects.create(name="DMZ")
    src1 = Source.objects.create(description="test desc", address=addr_pol1, service=svc_pol1, user=usr_pol1, zone=zone)
    src2 = Source.objects.create(
        address=addr_pol1,
        service=svc_pol1,
        user=usr_pol1,
    )
    src3 = Source.objects.create(address=addr_pol1, service=svc_pol1, zone=zone)
    dest1 = Destination.objects.create(description="test desc", address=addr_pol2, service=svc_pol2, zone=zone)
    dest2 = Destination.objects.create(
        address=addr_pol2,
        service=svc_pol2,
    )
    dest3 = Destination.objects.create(address=addr_pol3, service=svc_pol3, zone=zone)
    pol_rule1 = PolicyRule.objects.create(
        source=src1, destination=dest1, action="Deny", log=True, index=1, name="Policy Rule 1"
    )
    pol_rule2 = PolicyRule.objects.create(
        source=src2, destination=dest2, action="Allow", log=True, index=2, name="Policy Rule 2"
    )
    pol_rule3 = PolicyRule.objects.create(
        source=src3, destination=dest3, action="Drop", log=True, index=3, name="Policy Rule 3"
    )
    pol1 = Policy.objects.create(name="Policy 1")
    pol1.policy_rules.set([pol_rule1])
    pol2 = Policy.objects.create(name="Policy 2")
    pol2.policy_rules.set([pol_rule1, pol_rule2])
    pol3 = Policy.objects.create(name="Policy 3")
    pol3.policy_rules.set([pol_rule1, pol_rule2, pol_rule3])
