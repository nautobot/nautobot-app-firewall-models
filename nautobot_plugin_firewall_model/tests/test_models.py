"""Test VIPPartition model."""
# flake8: noqa: F403,405
from django.test import TestCase

from nautobot.ipam.models import VRF
from nautobot_plugin_firewall_model.models import *  # pylint: disable=unused-wildcard-import, wildcard-import


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

    def test_create_address_group_only_required(self):
        """Create AddressGroup with only required fields, and validate null description and __str__."""
        addr_grp = AddressGroup.objects.create(name="Development")

        self.assertEqual(addr_grp.description, "")
        self.assertEqual(addr_grp.name, "Development")
        self.assertEqual(addr_grp.ip_addresses.count(), 0)
        self.assertEqual(addr_grp.prefixes.count(), 0)
        self.assertEqual(addr_grp.ip_ranges.count(), 0)

    def test_create_address_group_ip_range_fields_success(self):
        """Create AddressGroup with ip_ranges & description fields."""
        ip_range = IPRange.objects.create(start_address="10.0.0.1", end_address="10.0.0.10")
        addr_grp = AddressGroup.objects.create(name="Development", description="development hosts")
        addr_grp.ip_ranges.add(ip_range)

        self.assertEqual(addr_grp.description, "development hosts")
        self.assertEqual(addr_grp.name, "Development")
        self.assertEqual(addr_grp.ip_addresses.count(), 0)
        self.assertEqual(addr_grp.prefixes.count(), 0)
        self.assertEqual(addr_grp.ip_ranges.first(), ip_range)

    def test_create_protocol_only_required(self):
        """Creates a protocol with only required fields."""
        protocol = Protocol.objects.create(name="HTTPS", port=443)

        self.assertEqual(protocol.description, "")
        self.assertEqual(protocol.name, "HTTPS")
        self.assertEqual(protocol.slug, "https")
        self.assertEqual(protocol.port, 443)
        self.assertEqual(str(protocol), "https:443")

    def test_create_protocol_all_fields(self):
        """Creates a protocol with all fields."""
        protocol = Protocol.objects.create(name="HTTPS", port=443, tcp_udp="tcp", description="Encrypted HTTP traffic")

        self.assertEqual(protocol.description, "Encrypted HTTP traffic")
        self.assertEqual(protocol.name, "HTTPS")
        self.assertEqual(protocol.slug, "https")
        self.assertEqual(protocol.port, 443)
        self.assertEqual(str(protocol), "https:443:tcp")

    def test_create_service_group_only_required(self):
        """Creates a service group with only required fields."""
        protocol = Protocol.objects.create(name="HTTPS", port=443)
        serv_grp = ServiceGroup.objects.create(name="Web")
        serv_grp.protocols.add(protocol)

        self.assertEqual(serv_grp.description, "")
        self.assertEqual(serv_grp.name, "Web")
        self.assertEqual(serv_grp.protocols.first(), protocol)
        self.assertEqual(str(serv_grp), "Web")

    def test_create_service_group_all_fields(self):
        """Creates a service group with all fields."""
        protocol = Protocol.objects.create(name="HTTPS", port=443)
        serv_grp = ServiceGroup.objects.create(name="Web", description="Web protocols")
        serv_grp.protocols.add(protocol)

        self.assertEqual(serv_grp.description, "Web protocols")
        self.assertEqual(serv_grp.name, "Web")
        self.assertEqual(serv_grp.protocols.first(), protocol)
        self.assertEqual(str(serv_grp), "Web")

    def test_create_user_only_required(self):
        """Creates a user with only required fields."""
        user = User.objects.create(username="user123")

        self.assertEqual(user.username, "user123")
        self.assertEqual(user.name, "")
        self.assertEqual(str(user), "user123")

    def test_create_user_all_fields(self):
        """Creates a user with all fields."""
        user = User.objects.create(username="user123", name="Foo Bar User")

        self.assertEqual(user.username, "user123")
        self.assertEqual(user.name, "Foo Bar User")
        self.assertEqual(str(user), "user123")

    def test_create_user_group_only_required(self):
        """Creates a user group with only required fields."""
        user = User.objects.create(username="user123")
        user_group = UserGroup.objects.create(name="group1")
        user_group.users.add(user)

        self.assertEqual(user_group.description, "")
        self.assertEqual(user_group.name, "group1")
        self.assertEqual(user_group.users.first(), user)
        self.assertEqual(str(user_group), "group1")

    def test_create_user_group_all_fields(self):
        """Creates a user group with all fields."""
        user = User.objects.create(username="user123", name="Foo Bar User")
        user_group = UserGroup.objects.create(name="group1", description="Test group 1.")
        user_group.users.add(user)

        self.assertEqual(user_group.description, "Test group 1.")
        self.assertEqual(user_group.name, "group1")
        self.assertEqual(user_group.users.first(), user)
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
