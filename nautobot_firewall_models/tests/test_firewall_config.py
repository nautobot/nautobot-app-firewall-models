"""Test Capirca Utils."""

# ruff: noqa: F403, F405
# pylint: disable=protected-access, too-many-lines
from io import StringIO
from unittest import skip
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import TestCase, override_settings
from nautobot.dcim.models import Device, Platform
from nautobot.extras.models import Status
from nautobot.ipam.models import IPAddress, Namespace

from nautobot_firewall_models import models
from nautobot_firewall_models.choices import FirewallConfigChoice
from nautobot_firewall_models.tests.fixtures import create_capirca_env, create_firewall_config_env
from nautobot_firewall_models.utils.aerleon import DevicePolicyToAerleon, PolicyToAerleon, generate_aerleon_config
from nautobot_firewall_models.utils.capirca import DevicePolicyToCapirca, PolicyToCapirca, generate_capirca_config

POLICY = """header {
  target:: cisco 150 extended
}

term allow-web-to-mail {
  source-address:: WEB_SERVERS
  destination-address:: MAIL_SERVERS
  destination-port:: SMTP
  protocol:: tcp
  action:: accept
}"""

SERVICES = """SMTP = 25/tcp"""

NETWORKS = """MAIL_SERVERS = 200.1.1.4/32
               200.1.1.5/32
WEB_SERVERS = 200.1.1.1/32"""

CFG = """! $Id:$
! $Date:$
! $Revision:$
no ip access-list extended 150
ip access-list extended 150
 remark $Id:$


 remark allow-web-to-mail
 permit tcp host 200.1.1.1 200.1.1.4 0.0.0.1 eq 25

exit
"""

NETWORKS2 = """addr-group1 = printer
              voice
addr-group3 = printer
              server
              storage
              voice
printer = 10.0.0.100/32
server = 10.1.0.0/24
storage = 10.0.0.0/24
voice = 10.0.0.1/32"""

SERVICES2 = """PGSQL = 5432/tcp
Source-HTTPS = 443/tcp
svc-group1 = PGSQL"""

POLICY2 = """header {
  target:: srx from-zone DMZ to-zone WAN
}

term Policy-Rule-1 {
  action:: deny
  comment:: "req1"
  destination-address:: addr-group3
  destination-address:: server
  destination-port:: PGSQL
  destination-port:: svc-group1
  logging:: true
  protocol:: tcp
  source-address:: addr-group1
  source-address:: printer
  source-port:: Source-HTTPS
}

header {
  target:: srx from-zone all to-zone all
}

term Test {
  action:: deny
  comment:: "req6"
  logging:: disable
}
"""

POLICYALL = """header {
  target:: srx from-zone DMZ to-zone WAN
}

term Policy-Rule-1 {
  action:: deny
  comment:: "req1"
  destination-address:: addr-group3
  destination-address:: server
  destination-port:: PGSQL
  destination-port:: svc-group1
  logging:: true
  protocol:: tcp
  source-address:: addr-group1
  source-address:: printer
  source-port:: Source-HTTPS
}

header {
  target:: srx from-zone WAN to-zone LAN
}

term Policy-Rule-2 {
  action:: accept
  comment:: "req2"
  destination-address:: addr-group3
  destination-address:: server
  destination-port:: PGSQL
  destination-port:: SSH
  destination-port:: svc-group1
  destination-port:: svc-group2
  logging:: true
  protocol:: tcp
  source-address:: addr-group1
  source-address:: addr-group2
  source-address:: printer
  source-address:: voice
}

header {
  target:: srx from-zone WAN to-zone LAN
}

term Policy-Rule-3 {
  action:: reject
  comment:: "req3"
  destination-address:: addr-group3
  destination-address:: server
  destination-port:: DNS
  destination-port:: PGSQL
  destination-port:: SSH
  destination-port:: svc-group1
  destination-port:: svc-group2
  destination-port:: svc-group3
  logging:: true
  protocol:: tcp
  source-address:: addr-group1
  source-address:: addr-group2
  source-address:: printer
  source-address:: storage
  source-address:: voice
}

header {
  target:: srx from-zone all to-zone all
}

term DENY-ALL {
  action:: deny
  comment:: "req5"
  logging:: disable
}

header {
  target:: srx from-zone DMZ to-zone WAN
}

term Policy-Rule-1 {
  action:: deny
  comment:: "req1"
  destination-address:: addr-group3
  destination-address:: server
  destination-port:: PGSQL
  destination-port:: svc-group1
  logging:: true
  protocol:: tcp
  source-address:: addr-group1
  source-address:: printer
  source-port:: Source-HTTPS
}

header {
  target:: srx from-zone DMZ to-zone WAN
}

term Policy-Rule-1 {
  action:: deny
  comment:: "req1"
  destination-address:: addr-group3
  destination-address:: server
  destination-port:: PGSQL
  destination-port:: svc-group1
  logging:: true
  protocol:: tcp
  source-address:: addr-group1
  source-address:: printer
  source-port:: Source-HTTPS
}

header {
  target:: srx from-zone WAN to-zone LAN
}

term Policy-Rule-2 {
  action:: accept
  comment:: "req2"
  destination-address:: addr-group3
  destination-address:: server
  destination-port:: PGSQL
  destination-port:: SSH
  destination-port:: svc-group1
  destination-port:: svc-group2
  logging:: true
  protocol:: tcp
  source-address:: addr-group1
  source-address:: addr-group2
  source-address:: printer
  source-address:: voice
}
"""

POLICY_DATA = [
    {
        "rule-name": "Policy Rule 1",
        "source-address": ["printer"],
        "source-group-address": ["addr group1"],
        "source-service": ["Source HTTPS"],
        "source-group-service": [],
        "from-zone": "DMZ",
        "destination-address": ["server"],
        "destination-group-address": ["addr group3"],
        "to-zone": "WAN",
        "destination-service": ["PGSQL"],
        "destination-group-service": ["svc group1"],
        "protocol": ["TCP"],
        "action": "deny",
        "logging": True,
        "request-id": "req1",
        "custom_field_data": {},
    },
    {
        "rule-name": "Test",
        "source-address": [],
        "source-group-address": [],
        "source-service": [],
        "source-group-service": [],
        "from-zone": "all",
        "destination-address": [],
        "destination-group-address": [],
        "to-zone": "all",
        "destination-service": [],
        "destination-group-service": [],
        "protocol": [],
        "action": "deny",
        "logging": False,
        "request-id": "req6",
        "custom_field_data": {},
    },
]


class TestBasicCapirca(TestCase):
    """Test models."""

    def setUp(self) -> None:
        """Setup test data."""
        create_capirca_env()

    def test_generate_capirca_config(self):
        """Test the implementation of capirca."""
        # This partially tests the underlying library, but kept since it helps ensure that overloading
        # ParseServiceList and ParseNetworkList continue to work. As well as provides an easy place to test locally.
        # Such as running `invoke unittest -l nautobot_firewall_models.tests.test_capirca.TestBasicCapirca` and
        # modifying data within test
        actual_cfg = generate_capirca_config(
            SERVICES.split("\n"), NETWORKS.split("\n"), POLICY, "capirca.lib.cisco.Cisco"
        )
        self.assertEqual(actual_cfg, CFG)


def _fake_custom_driver(device):  # pylint: disable=unused-argument
    """A fake custom driver for testing purposes."""
    return ("", "", "", "")


class TestPolicyToCapirca(TestCase):  # pylint: disable=too-many-public-methods,too-many-instance-attributes
    """Test models."""

    def setUp(self) -> None:
        """Setup test data."""
        create_capirca_env()
        self.active = Status.objects.get(name="Active")
        self.decomm = Status.objects.get(name="Decommissioned")
        self.device_obj = Device.objects.get(name="nyc-fw01")
        namespace = Namespace.objects.get(name="global")

        self.dev_name = self.device_obj.platform.network_driver
        zoneall = models.Zone.objects.get(name="all")

        self.pol_rule6 = models.PolicyRule.objects.create(
            name="Test", action="deny", log=False, request_id="req6", source_zone=zoneall, destination_zone=zoneall
        )
        self.pol1 = models.Policy.objects.get(name="Policy 1")
        self.pol1.policy_rules.add(self.pol_rule6)
        self.addr_obj4 = models.AddressObject.objects.get(name="server")
        self.ip_address = IPAddress.objects.create(address="10.0.0.101", namespace=namespace, status=self.active)
        self.addr_obj5 = models.AddressObject.objects.create(
            name="test-name", ip_address=self.ip_address, status=self.active
        )
        self.addr_grp3 = models.AddressObjectGroup.objects.get(name="addr group3")
        self.addr_grp4 = models.AddressObjectGroup.objects.create(name="test-group", status=self.active)
        self.addr_grp4.address_objects.set([self.addr_obj5])
        self.svc_obj4 = models.ServiceObject.objects.create(
            name="test-service", port="1800", ip_protocol="TCP", status=self.active
        )
        self.svc_grp4 = models.ServiceObjectGroup.objects.create(name="test-service-group", status=self.active)
        self.svc_grp4.service_objects.set([self.svc_obj4])

    def test_address_skip(self):
        """Check that address objects are found with status active and not found when other."""
        self.pol_rule6.source_addresses.set([self.addr_obj4, self.addr_obj5])
        self.pol_rule6.validated_save()
        _, networkdata, _ = PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()
        self.assertIn("test-name", networkdata)

        self.addr_obj5.status = self.decomm
        self.addr_obj5.validated_save()
        _, networkdata, _ = PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()
        self.assertNotIn("test-name", networkdata)

        self.pol_rule6.source_addresses.clear()
        self.addr_obj5.status = self.active
        self.addr_obj5.validated_save()

        self.pol_rule6.destination_addresses.set([self.addr_obj4, self.addr_obj5])
        self.pol_rule6.validated_save()
        _, networkdata, _ = PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()
        self.assertIn("test-name", networkdata)

        self.addr_obj5.status = self.decomm
        self.addr_obj5.validated_save()
        _, networkdata, _ = PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()
        self.assertNotIn("test-name", networkdata)

    def test_address_empty(self):
        """Check that when all address objects are removed, it fails."""
        self.pol_rule6.source_addresses.set([self.addr_obj5])
        self.addr_obj5.status = self.decomm
        self.addr_obj5.validated_save()
        with self.assertRaises(ValidationError):
            PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()
        self.pol_rule6.source_addresses.clear()
        self.pol_rule6.destination_addresses.set([self.addr_obj5])
        with self.assertRaises(ValidationError):
            PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()

    def test_address_fqdn(self):
        """Test that validation fails on creating an models.FQDN when using capirca."""
        fqdn1 = models.FQDN.objects.create(name="test.other", status=self.active)
        self.addr_obj5.ip_address = None
        self.addr_obj5.fqdn = fqdn1
        self.addr_obj5.validated_save()
        self.pol_rule6.source_addresses.set([self.addr_obj5])
        with self.assertRaises(ValidationError):
            PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()

    def test_address_ip_range(self):
        """Test that validation fails on creating an IP range when using capirca."""
        iprange1 = models.IPRange.objects.create(
            start_address="192.168.0.21", end_address="192.168.0.30", status=self.active
        )
        self.addr_obj5.ip_address = None
        self.addr_obj5.ip_range = iprange1
        self.addr_obj5.validated_save()
        self.pol_rule6.source_addresses.set([self.addr_obj5])
        with self.assertRaises(ValidationError):
            PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()

    def test_address_group_skip(self):
        """Check that address group objects are found with status active and not found when other."""
        self.pol_rule6.source_address_groups.set([self.addr_grp3, self.addr_grp4])
        self.pol_rule6.validated_save()
        _, networkdata, _ = PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()
        self.assertIn("test-group", networkdata)

        self.addr_grp4.status = self.decomm
        self.addr_grp4.validated_save()
        _, networkdata, _ = PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()
        self.assertNotIn("test-group", networkdata)

        self.pol_rule6.source_address_groups.clear()
        self.addr_grp4.status = self.active
        self.addr_grp4.validated_save()

        self.pol_rule6.destination_address_groups.set([self.addr_grp3, self.addr_grp4])
        self.pol_rule6.validated_save()
        _, networkdata, _ = PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()
        self.assertIn("test-group", networkdata)

        self.addr_grp4.status = self.decomm
        self.addr_grp4.validated_save()
        _, networkdata, _ = PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()
        self.assertNotIn("test-group", networkdata)

    def test_address_group_empty(self):
        """Check that when all address group objects are removed, it fails."""
        self.pol_rule6.source_address_groups.set([self.addr_grp4])
        self.addr_grp4.status = self.decomm
        self.addr_grp4.validated_save()
        with self.assertRaises(ValidationError):
            PolicyToCapirca(self.dev_name, self.pol1).validate_policy_data()
        self.pol_rule6.source_addresses.set([self.addr_obj5])
        self.pol_rule6.validated_save()
        obj = PolicyToCapirca(self.dev_name, self.pol1)
        obj.validate_policy_data()
        self.assertIn("test-name", obj.address)
        self.pol_rule6.destination_address_groups.clear()
        self.pol_rule6.destination_address_groups.set([self.addr_grp4])
        self.pol_rule6.validated_save()
        with self.assertRaises(ValidationError):
            PolicyToCapirca(self.dev_name, self.pol1).validate_policy_data()
        self.pol_rule6.destination_addresses.set([self.addr_obj5])
        self.pol_rule6.validated_save()
        obj = PolicyToCapirca(self.dev_name, self.pol1)
        obj.validate_policy_data()
        self.assertIn("test-name", obj.address)

    def test_address_group_skipped_member(self):
        """Check that an address group whose members are all inactive gets cleared."""
        namespace = Namespace.objects.get(name="global")
        ip_address6 = IPAddress.objects.create(address="10.0.0.102", status=self.active, namespace=namespace)
        addr_obj6 = models.AddressObject.objects.create(name="test-name6", ip_address=ip_address6, status=self.decomm)
        addr_grp6 = models.AddressObjectGroup.objects.create(name="test-group6", status=self.active)
        addr_grp6.address_objects.set([addr_obj6])
        self.pol_rule6.source_address_groups.set([addr_grp6])
        self.pol_rule6.validated_save()
        with self.assertRaises(ValidationError):
            PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()

        self.pol_rule6.source_address_groups.clear()
        self.pol_rule6.destination_address_groups.set([addr_grp6])
        self.pol_rule6.validated_save()
        with self.assertRaises(ValidationError):
            PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()

    def test_svcs_skip(self):
        """Check that service objects are found with status active and not found when other."""
        svc_obj2 = models.ServiceObject.objects.get(name="SSH")
        self.pol_rule6.destination_services.set([self.svc_obj4, svc_obj2])
        self.pol_rule6.validated_save()
        _, _, servicedata = PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()
        self.assertIn("test-service", servicedata)

        self.svc_obj4.status = self.decomm
        self.svc_obj4.validated_save()
        _, _, servicedata = PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()
        self.assertNotIn("test-service", servicedata)

    def test_svcs_skip_empty(self):
        """Check that when all service objects are removed, it fails."""
        self.pol_rule6.destination_services.set([self.svc_obj4])
        self.svc_obj4.status = self.decomm
        self.svc_obj4.validated_save()
        with self.assertRaises(ValidationError):
            PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()

    def test_svcs_group_skip(self):
        """Check that service objects are found with status active and not found when other."""
        svc_grp1 = models.ServiceObjectGroup.objects.get(name="svc group1")
        self.pol_rule6.destination_service_groups.set([self.svc_grp4, svc_grp1])
        self.pol_rule6.validated_save()
        _, _, servicedata = PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()
        self.assertIn("test-service-group", servicedata)

        self.svc_grp4.status = self.decomm
        self.svc_grp4.validated_save()
        _, _, servicedata = PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()
        self.assertNotIn("test-service-group", servicedata)

    def test_svcs_group_skip_empty(self):
        """Check that when all service objects are removed, it fails."""
        self.pol_rule6.destination_service_groups.set([self.svc_grp4])
        self.svc_grp4.status = self.decomm
        self.svc_grp4.validated_save()
        with self.assertRaises(ValidationError):
            PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()

    def test_svcs_group_skipped_member(self):
        """Check that a service group whose members are all inactive gets cleared."""
        self.svc_obj4.status = self.decomm
        self.svc_obj4.validated_save()
        self.pol_rule6.destination_service_groups.set([self.svc_grp4])
        self.pol_rule6.validated_save()
        with self.assertRaises(ValidationError):
            PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()
        svc_obj2 = models.ServiceObject.objects.get(name="SSH")
        self.pol_rule6.destination_services.set([svc_obj2])
        self.pol_rule6.validated_save()
        cap_obj = PolicyToCapirca(self.dev_name, self.pol1)
        cap_obj.validate_policy_data()
        self.assertIn("SSH", cap_obj.service)

    def test_svcs_ip_protocol_not_expected(self):
        """Check that you cannot mix and match tcp/udp that have ports with other protocols."""
        svc_obj5 = models.ServiceObject.objects.create(name="ICMP", ip_protocol="ICMP", status=self.active)
        self.pol_rule6.destination_services.set([self.svc_obj4, svc_obj5])
        self.pol_rule6.validated_save()
        with self.assertRaises(ValidationError):
            PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()

    def test_svcs_multi_proto_no_port(self):
        """Check that you can mix and match tcp/udp with other protocols, as long as no port."""
        svc_obj5 = models.ServiceObject.objects.create(name="ICMP", ip_protocol="ICMP", status=self.active)
        svc_obj6 = models.ServiceObject.objects.create(name="TCP", ip_protocol="TCP", status=self.active)
        self.pol_rule6.destination_services.set([svc_obj5, svc_obj6])
        self.pol_rule6.validated_save()
        pol, _, _ = PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()
        self.assertEqual(len(pol[1]["terms"]["destination-port"]), 0)
        self.assertEqual(pol[1]["terms"]["protocol"], ["icmp", "tcp"])

    def test_policy_skip(self):
        """Check that policy rules are found with status active and not found when other."""
        pol_rule5 = models.PolicyRule.objects.get(name="DENY ALL")
        self.pol1.policy_rules.add(pol_rule5)
        pol, _, _ = PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()
        self.assertIn("Test", [i["rule-name"] for i in pol])

        self.pol_rule6.status = self.decomm
        self.pol_rule6.validated_save()
        pol, _, _ = PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()
        self.assertNotIn("Test", [i["rule-name"] for i in pol])

    def test_policy_skip_empty(self):
        """Check that when all policy rules are removed, it fails."""
        self.pol_rule6.status = self.decomm
        self.pol_rule6.validated_save()
        pol1 = models.PolicyRule.objects.get(name="Policy Rule 1")
        pol1.status = self.decomm
        pol1.validated_save()
        with self.assertRaises(ValidationError):
            PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()

    def test_policy_remark_skipped(self):
        """Test when remaek is skipped over."""
        pol, _, _ = PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()
        self.assertIn("Test", [i["rule-name"] for i in pol])
        self.pol_rule6.action = "remark"
        self.pol_rule6.validated_save()
        pol, _, _ = PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()
        self.assertNotIn("Test", [i["rule-name"] for i in pol])

    @patch("nautobot_firewall_models.utils.capirca.PLUGIN_CFG", {"capirca_remark_pass": False})
    def test_policy_remark_fail(self):
        """Test when user configures to fail on remark."""
        self.pol_rule6.action = "remark"
        self.pol_rule6.validated_save()
        with self.assertRaises(ValidationError):
            PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()

    def test_policy_chd(self):
        """Test ability to inject custom headers."""
        self.pol_rule6._custom_field_data = {"chd_test-custom": "unique-value"}
        self.pol_rule6.save()
        pol, _, _ = PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()
        self.assertIn("unique-value", pol[1]["headers"])

    def test_policy_ctd(self):
        """Test ability to inject custom terms."""
        self.pol_rule6._custom_field_data = {"ctd_test-custom": "unique-value"}
        self.pol_rule6.save()
        pol, _, _ = PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()
        self.assertIn("test-custom", pol[1]["terms"])

    def test_policy_chd_allow_list(self):
        """Test headers can be allowed and not allowed based on custom field."""
        self.pol_rule6._custom_field_data = {"chd_test-custom": "unique-value", "chd_test-other": "other-value"}
        self.pol_rule6.save()
        self.device_obj.platform._custom_field_data = {"capirca_allow": ["chd_test-custom"]}
        self.device_obj.platform.save()
        pol, _, _ = PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()
        self.assertIn("unique-value", pol[1]["headers"])
        self.assertNotIn("other-value", pol[1]["headers"])

    def test_policy_ctd_allow_list(self):
        """Test terms can be allowed and not allowed based on custom field."""
        self.pol_rule6._custom_field_data = {"ctd_test-custom": "unique-value", "ctd_test-other": "other-value"}
        self.pol_rule6.save()
        self.device_obj.platform._custom_field_data = {"capirca_allow": ["ctd_test-custom"]}
        self.device_obj.platform.save()
        pol, _, _ = PolicyToCapirca(self.dev_name, self.pol1).validate_capirca_data()
        self.assertIn("test-custom", pol[1]["terms"])
        self.assertNotIn("test-other", pol[1]["terms"])

    def test_validate_policy_data(self):
        """Test validate_policy_data produces consistent results."""
        cap_obj = PolicyToCapirca(self.dev_name, self.pol1)
        cap_obj.validate_policy_data()
        self.assertEqual(cap_obj.policy, POLICY_DATA)

    def test_validate_policy_data_no_policy(self):
        """Test that it fails when you do not provied ability to get policy_detail obj."""
        with self.assertRaises(ValidationError):
            PolicyToCapirca(self.dev_name).validate_policy_data()

    def test_alt_capirca_type(self):
        """Test non-zone Capirca config generation."""
        Platform.objects.create(name="Cisco", network_driver="cisco")
        cap_obj = PolicyToCapirca("cisco", self.pol1)
        cap_obj.get_capirca_cfg()
        self.assertIn("cisco", cap_obj.pol_file)

    def test_validate_capirca_data_bad_platform(self):
        """Ensure that an error is raised if platform is not found."""
        Platform.objects.create(name="Fake Platform", network_driver="fake")
        with self.assertRaises(ValidationError):
            PolicyToCapirca("fake", self.pol1).validate_capirca_data()

    @override_settings(NETWORK_DRIVERS={"capirca": {"juniper_junos": "srx"}})
    def test_capirca_conversion(self):
        """Verify that generating full config for a policy is as expected."""
        cap_obj = PolicyToCapirca(self.dev_name, self.pol1)
        cap_obj.get_capirca_cfg()
        self.assertEqual(cap_obj.net_file, NETWORKS2)
        self.assertEqual(cap_obj.svc_file, SERVICES2)
        self.assertEqual(cap_obj.pol_file, POLICY2)


class TestDevicePolicyToCapirca(TestCase):
    """Test models."""

    def setUp(self) -> None:
        """Setup test data."""
        create_capirca_env()
        self.device_obj = Device.objects.get(name="nyc-fw01")

    @skip("Not implemented until policy method provided to merge queries provided")
    def test_dynamic_group_and_device(self):
        """Test that dynamic groups are created and device is added to it, disabled."""

    @override_settings(NETWORK_DRIVERS={"capirca": {"juniper_junos": "srx"}})
    def test_multi_policy_capirca_config(self):
        """Verify that generating full config for a device is as expected."""
        cap_obj = DevicePolicyToCapirca(self.device_obj)
        cap_obj.get_all_capirca_cfg()
        self.assertEqual(cap_obj.pol_file, POLICYALL)

    def test_multi_policy_skipped(self):
        """Ensure that when a policy is not active, it is removed from consideration."""
        cap_obj = DevicePolicyToCapirca(self.device_obj)
        cap_obj.get_all_capirca_cfg()
        self.assertEqual(len(cap_obj.policy), 7)
        decomm = Status.objects.get(name="Decommissioned")
        pol3 = models.Policy.objects.get(name="Policy 3")
        pol3.status = decomm
        pol3.validated_save()
        cap_obj = DevicePolicyToCapirca(self.device_obj)
        cap_obj.get_all_capirca_cfg()
        self.assertEqual(len(cap_obj.policy), 3)


class TestBasicAerleon(TestCase):
    """Test models."""

    def setUp(self) -> None:
        """Setup test data."""
        create_firewall_config_env()

    def test_generate_aerleon_config(self):
        """Test the implementation of aerleon."""
        # This partially tests the underlying library, but kept since it helps ensure that overloading
        # ParseServiceList and ParseNetworkList continue to work. As well as provides an easy place to test locally.
        # Such as running `invoke unittest -l nautobot_firewall_models.tests.test_aerleon.TestBasicAerleon` and
        # modifying data within test
        actual_cfg = generate_aerleon_config(
            SERVICES.split("\n"), NETWORKS.split("\n"), POLICY, "aerleon.lib.cisco.Cisco"
        )
        self.assertEqual(actual_cfg, CFG)


class TestPolicyToAerleon(TestCase):  # pylint: disable=too-many-public-methods,too-many-instance-attributes
    """Test models."""

    def setUp(self) -> None:
        """Setup test data."""
        create_firewall_config_env()
        self.active = Status.objects.get(name="Active")
        self.decomm = Status.objects.get(name="Decommissioned")
        self.device_obj = Device.objects.get(name="nyc-fw01")
        namespace = Namespace.objects.get(name="global")

        self.dev_name = self.device_obj.platform.network_driver
        zoneall = models.Zone.objects.get(name="all")

        self.pol_rule6 = models.PolicyRule.objects.create(
            name="Test", action="deny", log=False, request_id="req6", source_zone=zoneall, destination_zone=zoneall
        )
        self.pol1 = models.Policy.objects.get(name="Policy 1")
        self.pol1.policy_rules.add(self.pol_rule6)
        self.addr_obj4 = models.AddressObject.objects.get(name="server")
        self.ip_address = IPAddress.objects.create(address="10.0.0.101", namespace=namespace, status=self.active)
        self.addr_obj5 = models.AddressObject.objects.create(
            name="test-name", ip_address=self.ip_address, status=self.active
        )
        self.addr_grp3 = models.AddressObjectGroup.objects.get(name="addr group3")
        self.addr_grp4 = models.AddressObjectGroup.objects.create(name="test-group", status=self.active)
        self.addr_grp4.address_objects.set([self.addr_obj5])
        self.svc_obj4 = models.ServiceObject.objects.create(
            name="test-service", port="1800", ip_protocol="TCP", status=self.active
        )
        self.svc_grp4 = models.ServiceObjectGroup.objects.create(name="test-service-group", status=self.active)
        self.svc_grp4.service_objects.set([self.svc_obj4])

    def test_address_skip(self):
        """Check that address objects are found with status active and not found when other."""
        self.pol_rule6.source_addresses.set([self.addr_obj4, self.addr_obj5])
        self.pol_rule6.validated_save()
        _, networkdata, _ = PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()
        self.assertIn("test-name", networkdata)

        self.addr_obj5.status = self.decomm
        self.addr_obj5.validated_save()
        _, networkdata, _ = PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()
        self.assertNotIn("test-name", networkdata)

        self.pol_rule6.source_addresses.clear()
        self.addr_obj5.status = self.active
        self.addr_obj5.validated_save()

        self.pol_rule6.destination_addresses.set([self.addr_obj4, self.addr_obj5])
        self.pol_rule6.validated_save()
        _, networkdata, _ = PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()
        self.assertIn("test-name", networkdata)

        self.addr_obj5.status = self.decomm
        self.addr_obj5.validated_save()
        _, networkdata, _ = PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()
        self.assertNotIn("test-name", networkdata)

    def test_address_empty(self):
        """Check that when all address objects are removed, it fails."""
        self.pol_rule6.source_addresses.set([self.addr_obj5])
        self.addr_obj5.status = self.decomm
        self.addr_obj5.validated_save()
        with self.assertRaises(ValidationError):
            PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()
        self.pol_rule6.source_addresses.clear()
        self.pol_rule6.destination_addresses.set([self.addr_obj5])
        with self.assertRaises(ValidationError):
            PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()

    def test_address_fqdn(self):
        """Test that validation fails on creating an models.FQDN when using aerleon."""
        fqdn1 = models.FQDN.objects.create(name="test.other", status=self.active)
        self.addr_obj5.ip_address = None
        self.addr_obj5.fqdn = fqdn1
        self.addr_obj5.validated_save()
        self.pol_rule6.source_addresses.set([self.addr_obj5])
        with self.assertRaises(ValidationError):
            PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()

    def test_address_ip_range(self):
        """Test that validation fails on creating an IP range when using aerleon."""
        iprange1 = models.IPRange.objects.create(
            start_address="192.168.0.21", end_address="192.168.0.30", status=self.active
        )
        self.addr_obj5.ip_address = None
        self.addr_obj5.ip_range = iprange1
        self.addr_obj5.validated_save()
        self.pol_rule6.source_addresses.set([self.addr_obj5])
        with self.assertRaises(ValidationError):
            PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()

    def test_address_group_skip(self):
        """Check that address group objects are found with status active and not found when other."""
        self.pol_rule6.source_address_groups.set([self.addr_grp3, self.addr_grp4])
        self.pol_rule6.validated_save()
        _, networkdata, _ = PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()
        self.assertIn("test-group", networkdata)

        self.addr_grp4.status = self.decomm
        self.addr_grp4.validated_save()
        _, networkdata, _ = PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()
        self.assertNotIn("test-group", networkdata)

        self.pol_rule6.source_address_groups.clear()
        self.addr_grp4.status = self.active
        self.addr_grp4.validated_save()

        self.pol_rule6.destination_address_groups.set([self.addr_grp3, self.addr_grp4])
        self.pol_rule6.validated_save()
        _, networkdata, _ = PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()
        self.assertIn("test-group", networkdata)

        self.addr_grp4.status = self.decomm
        self.addr_grp4.validated_save()
        _, networkdata, _ = PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()
        self.assertNotIn("test-group", networkdata)

    def test_address_group_empty(self):
        """Check that when all address group objects are removed, it fails."""
        self.pol_rule6.source_address_groups.set([self.addr_grp4])
        self.addr_grp4.status = self.decomm
        self.addr_grp4.validated_save()
        with self.assertRaises(ValidationError):
            PolicyToAerleon(self.dev_name, self.pol1).validate_policy_data()
        self.pol_rule6.source_addresses.set([self.addr_obj5])
        self.pol_rule6.validated_save()
        obj = PolicyToAerleon(self.dev_name, self.pol1)
        obj.validate_policy_data()
        self.assertIn("test-name", obj.address)
        self.pol_rule6.destination_address_groups.clear()
        self.pol_rule6.destination_address_groups.set([self.addr_grp4])
        self.pol_rule6.validated_save()
        with self.assertRaises(ValidationError):
            PolicyToAerleon(self.dev_name, self.pol1).validate_policy_data()
        self.pol_rule6.destination_addresses.set([self.addr_obj5])
        self.pol_rule6.validated_save()
        obj = PolicyToAerleon(self.dev_name, self.pol1)
        obj.validate_policy_data()
        self.assertIn("test-name", obj.address)

    def test_address_group_skipped_member(self):
        """Check that an address group whose members are all inactive gets cleared."""
        namespace = Namespace.objects.get(name="global")
        ip_address6 = IPAddress.objects.create(address="10.0.0.102", status=self.active, namespace=namespace)
        addr_obj6 = models.AddressObject.objects.create(name="test-name6", ip_address=ip_address6, status=self.decomm)
        addr_grp6 = models.AddressObjectGroup.objects.create(name="test-group6", status=self.active)
        addr_grp6.address_objects.set([addr_obj6])
        self.pol_rule6.source_address_groups.set([addr_grp6])
        self.pol_rule6.validated_save()
        with self.assertRaises(ValidationError):
            PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()

        self.pol_rule6.source_address_groups.clear()
        self.pol_rule6.destination_address_groups.set([addr_grp6])
        self.pol_rule6.validated_save()
        with self.assertRaises(ValidationError):
            PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()

    def test_svcs_skip(self):
        """Check that service objects are found with status active and not found when other."""
        svc_obj2 = models.ServiceObject.objects.get(name="SSH")
        self.pol_rule6.destination_services.set([self.svc_obj4, svc_obj2])
        self.pol_rule6.validated_save()
        _, _, servicedata = PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()
        self.assertIn("test-service", servicedata)

        self.svc_obj4.status = self.decomm
        self.svc_obj4.validated_save()
        _, _, servicedata = PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()
        self.assertNotIn("test-service", servicedata)

    def test_svcs_skip_empty(self):
        """Check that when all service objects are removed, it fails."""
        self.pol_rule6.destination_services.set([self.svc_obj4])
        self.svc_obj4.status = self.decomm
        self.svc_obj4.validated_save()
        with self.assertRaises(ValidationError):
            PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()

    def test_svcs_group_skip(self):
        """Check that service objects are found with status active and not found when other."""
        svc_grp1 = models.ServiceObjectGroup.objects.get(name="svc group1")
        self.pol_rule6.destination_service_groups.set([self.svc_grp4, svc_grp1])
        self.pol_rule6.validated_save()
        _, _, servicedata = PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()
        self.assertIn("test-service-group", servicedata)

        self.svc_grp4.status = self.decomm
        self.svc_grp4.validated_save()
        _, _, servicedata = PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()
        self.assertNotIn("test-service-group", servicedata)

    def test_svcs_group_skip_empty(self):
        """Check that when all service objects are removed, it fails."""
        self.pol_rule6.destination_service_groups.set([self.svc_grp4])
        self.svc_grp4.status = self.decomm
        self.svc_grp4.validated_save()
        with self.assertRaises(ValidationError):
            PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()

    def test_svcs_group_skipped_member(self):
        """Check that a service group whose members are all inactive gets cleared."""
        self.svc_obj4.status = self.decomm
        self.svc_obj4.validated_save()
        self.pol_rule6.destination_service_groups.set([self.svc_grp4])
        self.pol_rule6.validated_save()
        with self.assertRaises(ValidationError):
            PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()
        svc_obj2 = models.ServiceObject.objects.get(name="SSH")
        self.pol_rule6.destination_services.set([svc_obj2])
        self.pol_rule6.validated_save()
        cap_obj = PolicyToAerleon(self.dev_name, self.pol1)
        cap_obj.validate_policy_data()
        self.assertIn("SSH", cap_obj.service)

    def test_svcs_ip_protocol_not_expected(self):
        """Check that you cannot mix and match tcp/udp that have ports with other protocols."""
        svc_obj5 = models.ServiceObject.objects.create(name="ICMP", ip_protocol="ICMP", status=self.active)
        self.pol_rule6.destination_services.set([self.svc_obj4, svc_obj5])
        self.pol_rule6.validated_save()
        with self.assertRaises(ValidationError):
            PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()

    def test_svcs_multi_proto_no_port(self):
        """Check that you can mix and match tcp/udp with other protocols, as long as no port."""
        svc_obj5 = models.ServiceObject.objects.create(name="ICMP", ip_protocol="ICMP", status=self.active)
        svc_obj6 = models.ServiceObject.objects.create(name="TCP", ip_protocol="TCP", status=self.active)
        self.pol_rule6.destination_services.set([svc_obj5, svc_obj6])
        self.pol_rule6.validated_save()
        pol, _, _ = PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()
        self.assertEqual(len(pol[1]["terms"]["destination-port"]), 0)
        self.assertEqual(pol[1]["terms"]["protocol"], ["icmp", "tcp"])

    def test_policy_skip(self):
        """Check that policy rules are found with status active and not found when other."""
        pol_rule5 = models.PolicyRule.objects.get(name="DENY ALL")
        self.pol1.policy_rules.add(pol_rule5)
        pol, _, _ = PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()
        self.assertIn("Test", [i["rule-name"] for i in pol])

        self.pol_rule6.status = self.decomm
        self.pol_rule6.validated_save()
        pol, _, _ = PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()
        self.assertNotIn("Test", [i["rule-name"] for i in pol])

    def test_policy_skip_empty(self):
        """Check that when all policy rules are removed, it fails."""
        self.pol_rule6.status = self.decomm
        self.pol_rule6.validated_save()
        pol1 = models.PolicyRule.objects.get(name="Policy Rule 1")
        pol1.status = self.decomm
        pol1.validated_save()
        with self.assertRaises(ValidationError):
            PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()

    def test_policy_remark_skipped(self):
        """Test when remaek is skipped over."""
        pol, _, _ = PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()
        self.assertIn("Test", [i["rule-name"] for i in pol])
        self.pol_rule6.action = "remark"
        self.pol_rule6.validated_save()
        pol, _, _ = PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()
        self.assertNotIn("Test", [i["rule-name"] for i in pol])

    @patch("nautobot_firewall_models.utils.aerleon.PLUGIN_CFG", {"aerleon_remark_pass": False})
    def test_policy_remark_fail(self):
        """Test when user configures to fail on remark."""
        self.pol_rule6.action = "remark"
        self.pol_rule6.validated_save()
        with self.assertRaises(ValidationError):
            PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()

    def test_policy_chd(self):
        """Test ability to inject custom headers."""
        self.pol_rule6._custom_field_data = {"chd_test-custom": "unique-value"}
        self.pol_rule6.save()
        pol, _, _ = PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()
        self.assertIn("unique-value", pol[1]["headers"])

    def test_policy_ctd(self):
        """Test ability to inject custom terms."""
        self.pol_rule6._custom_field_data = {"ctd_test-custom": "unique-value"}
        self.pol_rule6.save()
        pol, _, _ = PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()
        self.assertIn("test-custom", pol[1]["terms"])

    def test_policy_chd_allow_list(self):
        """Test headers can be allowed and not allowed based on custom field."""
        self.pol_rule6._custom_field_data = {"chd_test-custom": "unique-value", "chd_test-other": "other-value"}
        self.pol_rule6.save()
        self.device_obj.platform._custom_field_data = {"aerleon_allow": ["chd_test-custom"]}
        self.device_obj.platform.save()
        pol, _, _ = PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()
        self.assertIn("unique-value", pol[1]["headers"])
        self.assertNotIn("other-value", pol[1]["headers"])

    def test_policy_ctd_allow_list(self):
        """Test terms can be allowed and not allowed based on custom field."""
        self.pol_rule6._custom_field_data = {"ctd_test-custom": "unique-value", "ctd_test-other": "other-value"}
        self.pol_rule6.save()
        self.device_obj.platform._custom_field_data = {"aerleon_allow": ["ctd_test-custom"]}
        self.device_obj.platform.save()
        pol, _, _ = PolicyToAerleon(self.dev_name, self.pol1).validate_aerleon_data()
        self.assertIn("test-custom", pol[1]["terms"])
        self.assertNotIn("test-other", pol[1]["terms"])

    def test_validate_policy_data(self):
        """Test validate_policy_data produces consistent results."""
        cap_obj = PolicyToAerleon(self.dev_name, self.pol1)
        cap_obj.validate_policy_data()
        self.assertEqual(cap_obj.policy, POLICY_DATA)

    def test_validate_policy_data_no_policy(self):
        """Test that it fails when you do not provied ability to get policy_detail obj."""
        with self.assertRaises(ValidationError):
            PolicyToAerleon(self.dev_name).validate_policy_data()

    def test_alt_aerleon_type(self):
        """Test non-zone Aerleon config generation."""
        Platform.objects.create(name="cisco", network_driver="cisco_ios")
        cap_obj = PolicyToAerleon("cisco_ios", self.pol1)
        cap_obj.get_aerleon_cfg()
        self.assertIn("cisco", cap_obj.pol_file)

    def test_validate_aerleon_data_bad_platform(self):
        """Ensure that an error is raised if platform is not found."""
        Platform.objects.create(name="Fake Platform", network_driver="fake")
        with self.assertRaises(ValidationError):
            PolicyToAerleon("fake", self.pol1).validate_aerleon_data()

    @override_settings(NETWORK_DRIVERS={"aerleon": {"juniper_junos": "srx"}})
    def test_aerleon_conversion(self):
        """Verify that generating full config for a policy is as expected."""
        cap_obj = PolicyToAerleon(self.dev_name, self.pol1)
        cap_obj.get_aerleon_cfg()
        self.assertEqual(cap_obj.net_file, NETWORKS2)
        self.assertEqual(cap_obj.svc_file, SERVICES2)
        self.assertEqual(cap_obj.pol_file, POLICY2)


class TestDevicePolicyToAerleon(TestCase):
    """Test models."""

    def setUp(self) -> None:
        """Setup test data."""
        create_firewall_config_env()
        self.device_obj = Device.objects.get(name="nyc-fw01")

    @skip("Not implemented until policy method provided to merge queries provided")
    def test_dynamic_group_and_device(self):
        """Test that dynamic groups are created and device is added to it, disabled."""

    @override_settings(NETWORK_DRIVERS={"aerleon": {"juniper_junos": "srx"}})
    def test_multi_policy_aerleon_config(self):
        """Verify that generating full config for a device is as expected."""
        cap_obj = DevicePolicyToAerleon(self.device_obj)
        cap_obj.get_all_aerleon_cfg()
        self.assertEqual(cap_obj.pol_file, POLICYALL)

    def test_multi_policy_skipped(self):
        """Ensure that when a policy is not active, it is removed from consideration."""
        cap_obj = DevicePolicyToAerleon(self.device_obj)
        cap_obj.get_all_aerleon_cfg()
        self.assertEqual(len(cap_obj.policy), 7)
        decomm = Status.objects.get(name="Decommissioned")
        pol3 = models.Policy.objects.get(name="Policy 3")
        pol3.status = decomm
        pol3.validated_save()
        cap_obj = DevicePolicyToAerleon(self.device_obj)
        cap_obj.get_all_aerleon_cfg()
        self.assertEqual(len(cap_obj.policy), 3)


class TestCapircaToFirewallConfigMigration(TestCase):
    """Test models."""

    def setUp(self) -> None:
        """Setup test data."""
        create_capirca_env()

    def test_platform_not_set_correctly(self):
        """Test that CapircaPolicy is skipped if platform mapping is not correct."""
        # Set device platform to something not in CAPIRCA_MAPPER
        device = Device.objects.get(name="nyc-fw01")
        device.platform.network_driver = (
            "srx"  # Simulate a platform that works in capirca but not no in network_drivers
        )
        device.platform.save()
        models.CapircaPolicy.objects.create(device=device)
        # Should be skipped
        out = StringIO()
        call_command("capirca_to_fw_config_migration", stdout=out)
        self.assertIn("skipped: platform", out.getvalue())
        # No FirewallConfig should be created
        self.assertFalse(models.FirewallConfig.objects.filter(device=device).exists())

    @override_settings(
        PLUGINS_CONFIG={"nautobot_firewall_models": {"default_driver": FirewallConfigChoice.TYPE_CAPIRCA}}
    )
    def test_migration_for_capirca(self):
        """Test migration for capirca driver."""
        self._migration_helper(FirewallConfigChoice.TYPE_CAPIRCA)

    @override_settings(
        PLUGINS_CONFIG={"nautobot_firewall_models": {"default_driver": FirewallConfigChoice.TYPE_AERLEON}}
    )
    def test_migration_for_aerleon(self):
        """Test migration for aerleon driver."""
        self._migration_helper(FirewallConfigChoice.TYPE_AERLEON)

    @override_settings(
        PLUGINS_CONFIG={
            "nautobot_firewall_models": {
                "default_driver": FirewallConfigChoice.TYPE_CUSTOM,
                "custom_firewall_config": "nautobot_firewall_models.tests.test_firewall_config._fake_custom_driver",
            }
        }
    )
    @patch(
        "nautobot_firewall_models.constants.PLUGIN_CFG",
        {
            "default_driver": FirewallConfigChoice.TYPE_CUSTOM,
            "custom_firewall_config": "nautobot_firewall_models.tests.test_firewall_config._fake_custom_driver",
        },
    )
    @patch(
        "nautobot_firewall_models.models.firewall_config.PLUGIN_CFG",
        {
            "default_driver": FirewallConfigChoice.TYPE_CUSTOM,
            "custom_firewall_config": "nautobot_firewall_models.tests.test_firewall_config._fake_custom_driver",
        },
    )
    def test_migration_for_custom(self):
        """Test migration for custom driver."""
        self._migration_helper(FirewallConfigChoice.TYPE_CUSTOM)

    def _migration_helper(self, driver):
        device = Device.objects.get(name="nyc-fw01")
        models.FirewallConfig.objects.filter(device=device).delete()
        # Ensure CapircaPolicy exists
        if not models.CapircaPolicy.objects.filter(device=device).exists():
            models.CapircaPolicy.objects.create(device=device)
        out = StringIO()
        call_command("capirca_to_fw_config_migration", "--commit", stdout=out)
        self.assertIn(f"Migrated CapircaPolicy for device {device}", out.getvalue())
        fw = models.FirewallConfig.objects.get(device=device)
        self.assertEqual(fw.firewall_config_type, driver)

    def test_skip_already_migrated(self):
        """Test that migration skips devices already migrated."""
        device = Device.objects.get(name="nyc-fw01")
        # Ensure both CapircaPolicy and FirewallConfig exist
        models.CapircaPolicy.objects.get_or_create(device=device)
        models.FirewallConfig.objects.get_or_create(device=device)
        out = StringIO()
        call_command("capirca_to_fw_config_migration", "--commit", stdout=out)
        self.assertIn("already exists for device", out.getvalue())

    def test_dry_run_and_commit(self):
        """Test dry-run (no changes) and commit (writes changes) modes."""
        device = Device.objects.get(name="nyc-fw01")
        # Remove any existing FirewallConfig
        models.FirewallConfig.objects.filter(device=device).delete()
        models.CapircaPolicy.objects.create(device=device)
        # Dry run
        out = StringIO()
        call_command("capirca_to_fw_config_migration", stdout=out)
        self.assertIn("Dry run mode", out.getvalue())
        self.assertIn("Would migrate CapircaPolicy for device", out.getvalue())
        self.assertFalse(models.FirewallConfig.objects.filter(device=device).exists())
        # Commit
        out = StringIO()
        call_command("capirca_to_fw_config_migration", "--commit", stdout=out)
        self.assertIn("Migrated CapircaPolicy for device", out.getvalue())
        self.assertTrue(models.FirewallConfig.objects.filter(device=device).exists())
