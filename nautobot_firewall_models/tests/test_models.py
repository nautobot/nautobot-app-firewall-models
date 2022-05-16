"""Test Firewall models."""
# flake8: noqa: F403,405
from django.core.exceptions import ValidationError
from django.test import TestCase
from nautobot.ipam.models import VRF
from nautobot.extras.models import Status

from nautobot_firewall_models.models import *  # pylint: disable=unused-wildcard-import, wildcard-import


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
        self.assertEqual(str(protocol), "HTTPS")

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
        self.assertEqual(str(protocol), "HTTPS")

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
    """I hate writing docs strings easter egg."""

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

    def test_service_port_null(self):
        """Test port null."""
        svc = ServiceObject.objects.create(name="HTTP", ip_protocol="TCP", status=Status.objects.get(name="Active"))

        self.assertEqual(svc.port, None)

    def test_service_port_range_invalid(self):
        """Test port range."""
        with self.assertRaises(ValidationError):
            ServiceObject.objects.create(
                name="HTTP", port="8080-8088-999", ip_protocol="TCP", status=Status.objects.get(name="Active")
            )
