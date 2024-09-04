"""Test Firewall models."""

# ruff: noqa: F403, F405
# pylint: disable=invalid-name
from django.core.exceptions import ValidationError
from django.test import TestCase
from nautobot.dcim.models import Device
from nautobot.extras.models import Status
from nautobot.ipam.models import VRF

from nautobot_firewall_models.models import *  # pylint: disable=unused-wildcard-import, wildcard-import

from . import fixtures


class TestModels(TestCase):
    """Test models."""

    def setUp(self) -> None:
        """Setup test data."""
        self.vrf = VRF.objects.create(name="Development")

    def test_create_iprange_only_required(self):
        """Create IPRange with only required fields, and validate null description and __str__."""
        iprange = IPRange.objects.create(start_address="10.0.0.1", end_address="10.0.0.5")

        self.assertEqual(iprange.start_address, "10.0.0.1")
        self.assertEqual(iprange.end_address, "10.0.0.5")
        self.assertEqual(iprange.description, "")
        self.assertEqual(str(iprange), "10.0.0.1-10.0.0.5")
        self.assertEqual(iprange.vrf, None)
        self.assertEqual(iprange.size, 5)

    def test_create_iprange_all_fields_success(self):
        """Create IPRange with all fields."""
        iprange = IPRange.objects.create(
            start_address="10.0.0.1", end_address="10.0.0.5", description="Development", vrf=self.vrf
        )

        self.assertEqual(iprange.start_address, "10.0.0.1")
        self.assertEqual(iprange.end_address, "10.0.0.5")
        self.assertEqual(iprange.description, "Development")
        self.assertEqual(str(iprange), "10.0.0.1-10.0.0.5")
        self.assertEqual(iprange.vrf, self.vrf)
        self.assertEqual(iprange.size, 5)

    def test_iprange_missing_required_attr(self):
        """Test missing start_address."""
        with self.assertRaises(ValidationError):
            IPRange.objects.create(end_address="10.0.0.5", description="Development", vrf=self.vrf)

    def test_iprange_invalid_range(self):
        """Test missing start_address."""
        with self.assertRaises(ValidationError):
            IPRange.objects.create(
                start_address="10.0.0.15", end_address="10.0.0.5", description="Development", vrf=self.vrf
            )

    def test_create_zone_only_required(self):
        """Create Zone with only required fields, and validate null description and __str__."""
        zone = Zone.objects.create(name="trust")

        self.assertEqual(zone.description, "")
        self.assertEqual(zone.name, "trust")
        self.assertEqual(zone.interfaces.count(), 0)
        self.assertEqual(zone.vrfs.count(), 0)

    def test_create_zone_vrf_description_fields_success(self):
        """Create Zone with vrf & description fields."""
        zone = Zone.objects.create(name="trust", description="LAN Zone")
        zone.vrfs.add(self.vrf)

        self.assertEqual(zone.description, "LAN Zone")
        self.assertEqual(zone.name, "trust")
        self.assertEqual(zone.interfaces.count(), 0)
        self.assertEqual(zone.vrfs.first(), self.vrf)

    def test_address_object_too_many_objects(self):
        """Tests to make sure only one address can be on an address object."""
        fqdn = FQDN.objects.create(name="test.local")
        iprange = IPRange.objects.create(start_address="10.0.0.1", end_address="10.0.0.5")

        with self.assertRaises(ValidationError):
            AddressObject.objects.create(name="failure", fqdn=fqdn, ip_range=iprange)

    def test_create_protocol_only_required(self):
        """Creates a protocol with only required fields."""
        protocol = ServiceObject.objects.create(
            name="HTTPS", port="8443", ip_protocol="TCP", status=Status.objects.get(name="Active")
        )

        self.assertEqual(protocol.description, "")
        self.assertEqual(protocol.name, "HTTPS")
        self.assertEqual(protocol.port, "8443")
        self.assertEqual(str(protocol), "HTTPS (TCP/8443)")

    def test_create_protocol_all_fields(self):
        """Creates a protocol with all fields."""
        protocol = ServiceObject.objects.create(
            name="HTTPS",
            port="8443",
            ip_protocol="TCP",
            status=Status.objects.get(name="Active"),
            description="Encrypted HTTP traffic",
        )

        self.assertEqual(protocol.description, "Encrypted HTTP traffic")
        self.assertEqual(protocol.name, "HTTPS")
        self.assertEqual(protocol.port, "8443")
        self.assertEqual(str(protocol), "HTTPS (TCP/8443)")

    def test_create_service_group_only_required(self):
        """Creates a service group with only required fields."""
        protocol = ServiceObject.objects.create(
            name="HTTPS", port="8443", ip_protocol="TCP", status=Status.objects.get(name="Active")
        )
        serv_grp = ServiceObjectGroup.objects.create(name="Web")
        serv_grp.service_objects.add(protocol)

        self.assertEqual(serv_grp.description, "")
        self.assertEqual(serv_grp.name, "Web")
        self.assertEqual(serv_grp.service_objects.first(), protocol)
        self.assertEqual(str(serv_grp), "Web")

    def test_create_service_group_all_fields(self):
        """Creates a service group with all fields."""
        protocol = ServiceObject.objects.create(
            name="HTTPS", port="8443", ip_protocol="TCP", status=Status.objects.get(name="Active")
        )
        serv_grp = ServiceObjectGroup.objects.create(name="Web", description="Web protocols")
        serv_grp.service_objects.add(protocol)

        self.assertEqual(serv_grp.description, "Web protocols")
        self.assertEqual(serv_grp.name, "Web")
        self.assertEqual(serv_grp.service_objects.first(), protocol)
        self.assertEqual(str(serv_grp), "Web")

    def test_create_user_only_required(self):
        """Creates a user with only required fields."""
        user = UserObject.objects.create(username="user123")

        self.assertEqual(user.username, "user123")
        self.assertEqual(user.name, "")
        self.assertEqual(str(user), "user123")

    def test_create_user_all_fields(self):
        """Creates a user with all fields."""
        user = UserObject.objects.create(username="user123", name="Foo Bar User")

        self.assertEqual(user.username, "user123")
        self.assertEqual(user.name, "Foo Bar User")
        self.assertEqual(str(user), "user123")

    def test_create_user_group_only_required(self):
        """Creates a user group with only required fields."""
        user = UserObject.objects.create(username="user123")
        user_group = UserObjectGroup.objects.create(name="group1")
        user_group.user_objects.add(user)

        self.assertEqual(user_group.description, "")
        self.assertEqual(user_group.name, "group1")
        self.assertEqual(user_group.user_objects.first(), user)
        self.assertEqual(str(user_group), "group1")

    def test_create_user_group_all_fields(self):
        """Creates a user group with all fields."""
        user = UserObject.objects.create(username="user123", name="Foo Bar User")
        user_group = UserObjectGroup.objects.create(name="group1", description="Test group 1.")
        user_group.user_objects.add(user)

        self.assertEqual(user_group.description, "Test group 1.")
        self.assertEqual(user_group.name, "group1")
        self.assertEqual(user_group.user_objects.first(), user)
        self.assertEqual(str(user_group), "group1")

    def test_create_fqdn_only_required(self):
        """Creates a fqdn with only required fields."""
        fqdn = FQDN.objects.create(name="test.local")

        self.assertEqual(fqdn.description, "")
        self.assertEqual(fqdn.name, "test.local")

    def test_create_fqdn_all_fields(self):
        """Creates a fqdn with all fields."""
        fqdn = FQDN.objects.create(name="test.local", description="test domain")

        self.assertEqual(fqdn.description, "test domain")
        self.assertEqual(fqdn.name, "test.local")


class TestServiceObject(TestCase):
    """Test ServiceObjects."""

    def test_service_port(self):
        """Test single port."""
        svc = ServiceObject.objects.create(
            name="HTTP", port="8088", ip_protocol="TCP", status=Status.objects.get(name="Active")
        )

        self.assertEqual(svc.port, "8088")

    def test_service_port_range(self):
        """Test port range."""
        svc = ServiceObject.objects.create(
            name="HTTP", port="8080-8088", ip_protocol="TCP", status=Status.objects.get(name="Active")
        )

        self.assertEqual(svc.port, "8080-8088")

    def test_service_port_empty(self):
        """Test port empty string."""
        svc = ServiceObject.objects.create(
            name="HTTP", port="", ip_protocol="TCP", status=Status.objects.get(name="Active")
        )

        self.assertEqual(svc.port, "")

    def test_service_port_omitted_equals_blank(self):
        """Test port blank."""
        svc = ServiceObject.objects.create(name="HTTP", ip_protocol="TCP", status=Status.objects.get(name="Active"))

        self.assertEqual(svc.port, "")

    def test_service_port_range_invalid(self):
        """Test port range."""
        with self.assertRaises(ValidationError):
            ServiceObject.objects.create(
                name="HTTP", port="8080-8088-999", ip_protocol="TCP", status=Status.objects.get(name="Active")
            )


class TestPolicyRuleModels(TestCase):
    """Test the PolicyRule model."""

    def setUp(self) -> None:
        """Create the data."""
        fixtures.create_policy_rule()

    def test_policyrule_rule_details(self):
        """Test method rule_details on PolicyRule model."""
        rule_details = PolicyRule.objects.first().rule_details()
        self.assertEqual(rule_details["log"], True)
        # sample a few keys to ensure they are in there, more complete test in to_json test
        keys = ["rule", "source_address_groups", "destination_address_groups", "action"]
        self.assertTrue(set(keys).issubset(rule_details.keys()))

    def test_policyrule_to_json(self):
        """Test method to_json on PolicyRule model."""
        obj = PolicyRule.objects.first()
        json_details = obj.to_json()
        self.assertEqual(json_details["display"], "Policy Rule 1 - req1")
        self.assertTrue(obj.source_users.filter(id=json_details["source_users"][0]["id"]).exists())
        self.assertTrue(obj.source_user_groups.filter(id=json_details["source_user_groups"][0]["id"]).exists())
        self.assertTrue(obj.source_addresses.filter(id=json_details["source_addresses"][0]["id"]).exists())
        self.assertTrue(obj.source_address_groups.filter(id=json_details["source_address_groups"][0]["id"]).exists())
        self.assertTrue(obj.destination_services.filter(id=json_details["destination_services"][0]["id"]).exists())


class TestPolicyModels(TestCase):
    """Test the Policy model."""

    def setUp(self) -> None:
        """Create the data."""
        fixtures.create_policy()

    def test_policy_policy_details(self):
        """Test method policy_details on Policy model."""
        policy_details = Policy.objects.first().policy_details[0]
        self.assertEqual(policy_details["log"], True)
        # sample a few keys to ensure they are in there, more complete test in to_json test
        keys = ["rule", "source_address_groups", "destination_address_groups", "action"]
        self.assertTrue(set(keys).issubset(policy_details.keys()))

    def test_policy_to_json(self):
        """Test method to_json on Policy model."""
        obj = Policy.objects.all()[2]
        json_details = obj.to_json()["policy_rules"][2]
        self.assertTrue(obj.policy_rules.filter(id=json_details["id"]).exists())


class TestNATPolicyRuleModels(TestCase):
    """Test the NATPolicyRule model."""

    def setUp(self) -> None:
        """Create the data."""
        fixtures.create_natpolicy_rule()

    def test_natpolicyrule_rule_details(self):
        """Test method rule_details on NATPolicyRule model."""
        rule_details = NATPolicyRule.objects.first().rule_details()
        self.assertEqual(rule_details["log"], True)
        # sample a few keys to ensure they are in there, more complete test in to_json test
        keys = ["rule", "original_source_address_groups", "translated_destination_address_groups", "remark"]
        self.assertTrue(set(keys).issubset(rule_details.keys()))

    def test_natpolicyrule_to_json(self):
        """Test method to_json on NATPolicyRule model."""
        obj = NATPolicyRule.objects.first()
        json_details = obj.to_json()
        self.assertEqual(json_details["display"], "NAT Policy Rule 1.1 - req1")
        self.assertTrue(
            obj.original_destination_services.filter(id=json_details["original_destination_services"][0]["id"]).exists()
        )
        self.assertTrue(
            obj.translated_destination_services.filter(
                id=json_details["translated_destination_services"][0]["id"]
            ).exists()
        )


class TestNATPolicyModels(TestCase):
    """Test the NATPolicy model."""

    def setUp(self) -> None:
        """Create the data."""
        fixtures.create_natpolicy()

    def test_policy_policy_details(self):
        """Test method policy_details on Policy model."""
        policy_details = NATPolicy.objects.first().policy_details[0]
        self.assertEqual(policy_details["log"], True)
        # sample a few keys to ensure they are in there, more complete test in to_json test
        keys = ["rule", "original_source_address_groups", "original_destination_address_groups", "remark"]
        self.assertTrue(set(keys).issubset(policy_details.keys()))

    def test_policy_to_json(self):
        """Test method to_json on Policy model."""
        obj = NATPolicyRule.objects.first()
        json_details = obj.to_json()
        self.assertEqual(json_details["name"], "NAT Policy Rule 1.1")
        self.assertTrue(
            obj.original_destination_services.filter(id=json_details["original_destination_services"][0]["id"]).exists()
        )
        self.assertTrue(
            obj.translated_destination_services.filter(
                id=json_details["translated_destination_services"][0]["id"]
            ).exists()
        )


class TestCapircaModels(TestCase):
    """Test the Capirca model."""

    def setUp(self) -> None:
        """Create the data."""
        fixtures.create_capirca_env()

    def test_capirca_creates_model(self):
        """Test method to create model."""
        device_obj = Device.objects.get(name="DFW02-WAN00")
        cap_obj = CapircaPolicy.objects.create(device=device_obj)
        svc = "PGSQL = 5432/tcp"
        self.assertIn(svc, cap_obj.svc)
        net = "printer = 10.0.0.100/32"
        self.assertIn(net, cap_obj.net)
        pol = "target:: srx from-zone all to-zone all"
        self.assertIn(pol, cap_obj.pol)
