"""Unit tests for API views."""
from nautobot.ipam.models import Prefix
from nautobot.utilities.testing import APIViewTestCases

from nautobot_plugin_firewall_model.models import (
    IPRange,
    Zone,
    AddressGroup,
    Protocol,
    ServiceGroup,
    User,
    UserGroup,
)


class IPRangeAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the IPRange viewsets."""
    model = IPRange
    create_data = [
        {"start_address": "10.0.0.1", "end_address": "10.0.0.3"},
        {"start_address": "10.0.0.4", "end_address": "10.0.0.10"},
    ]
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        IPRange.objects.create(start_address="192.168.0.1", end_address="192.168.0.10")
        IPRange.objects.create(start_address="192.168.0.11", end_address="192.168.0.20")
        IPRange.objects.create(start_address="192.168.0.21", end_address="192.168.0.30")

    def test_list_objects_brief(self):
        pass


class ZoneAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the Zone viewsets."""
    model = Zone
    create_data = [
        {"name": "trust"},
        {"name": "untrust"},
    ]
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        Zone.objects.create(name="WAN")
        Zone.objects.create(name="LAN")
        Zone.objects.create(name="DMZ")

    def test_list_objects_brief(self):
        pass


class AddressGroupAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the AddressGroup viewsets."""
    model = AddressGroup
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        ip_range = IPRange.objects.create(start_address="192.168.0.1", end_address="192.168.0.10")
        prefix1 = Prefix.objects.create(network="10.0.0.0", prefix_length=24)
        prefix2 = Prefix.objects.create(network="10.0.2.0", prefix_length=24)
        AddressGroup.objects.create(name="data")
        AddressGroup.objects.create(name="voice")
        AddressGroup.objects.create(name="storage")

        cls.create_data = [
            {"name": "group1", "ip_ranges": [ip_range.id]},
            {"name": "group2", "ip_ranges": [ip_range.id], "prefixes": [prefix1.id, prefix2.id]},
        ]

    def test_list_objects_brief(self):
        pass


class ProtocolAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the Protocol viewsets."""
    model = Protocol
    bulk_update_data = {"description": "test update description"}
    create_data = [
        {"name": "HTTP", "port": 80},
        {"name": "HTTP", "port": 8080},
    ]
    choices_fields = ["tcp_udp"]

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        Protocol.objects.create(name="PGSQL", port=5432)
        Protocol.objects.create(name="SSH", port=22)
        Protocol.objects.create(name="TELNET", port=23)

    def test_list_objects_brief(self):
        pass


class ServiceGroupAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the ServiceGroup viewsets."""
    model = ServiceGroup
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        protocol = Protocol.objects.create(name="PGSQL", port=5432)
        for i in ["PGSQL", "DEVPGSQL", "UATPGSQL"]:
            serv_grp = ServiceGroup.objects.create(name=i)
            serv_grp.protocols.add(protocol)
        cls.create_data = [
            {"name": "test1", "protocols": [protocol.id]},
            {"name": "test2", "protocols": [protocol.id]},
        ]

    def test_list_objects_brief(self):
        pass


class UserAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the User viewsets."""
    model = User
    bulk_update_data = {"name": "User Name 123"}
    create_data = [
        {"username": "test1", "name": "Foo"},
        {"username": "test2", "name": "Bar"},
    ]

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        User.objects.create(username="user1")
        User.objects.create(username="user2")
        User.objects.create(username="user3")

    def test_list_objects_brief(self):
        pass


class UserGroupAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the UserGroup viewsets."""
    model = UserGroup
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        user = User.objects.create(username="user1")
        for i in range(3):
            user_group = UserGroup.objects.create(name=f"group{i}")
            user_group.users.add(user)
        cls.create_data = [
            {"name": "test1", "users": [user.id]},
            {"name": "test2", "users": [user.id]},
        ]

    def test_list_objects_brief(self):
        pass
