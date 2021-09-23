"""Unit tests for API views."""
# flake8: noqa: F403,405
from nautobot.utilities.testing import APIViewTestCases
from nautobot.ipam.models import Prefix

from nautobot_firewall_models.models import *  # pylint: disable=unused-wildcard-import, wildcard-import
from .fixtures import create_env


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
        create_env()

    def test_list_objects_brief(self):
        pass


class FQDNAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the Protocol viewsets."""
    model = FQDN
    bulk_update_data = {"description": "test update description"}
    create_data = [
        {"name": "test.local"},
        {"name": "sub.test.local"},
    ]

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()

    def test_list_objects_brief(self):
        pass


class AddressObjectAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the AddressObject viewsets."""
    model = AddressObject
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        ip_range = IPRange.objects.first()
        prefix = Prefix.objects.first()

        cls.create_data = [
            {"name": "obj1", "ip_range": ip_range.id},
            {"name": "obj2", "prefix": prefix.id},
        ]

    def test_list_objects_brief(self):
        pass


class AddressObjectGroupAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the AddressObjectGroup viewsets."""
    model = AddressObjectGroup
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        addr_obj = AddressObject.objects.first()
        cls.create_data = [
            {"name": "test1", "address_objects": [addr_obj.id]},
            {"name": "test2", "address_objects": [addr_obj.id]},
        ]

    def test_list_objects_brief(self):
        pass


class AddressPolicyObjectAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the AddressPolicyObject viewsets."""
    model = AddressPolicyObject
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        addr_obj = AddressObject.objects.first()
        addr_grp = AddressObjectGroup.objects.first()
        cls.create_data = [
            {"name": "test1", "address_objects": [addr_obj.id]},
            {"name": "test2", "address_object_groups": [addr_grp.id]},
            {"name": "test3", "address_objects": [addr_obj.id], "address_object_groups": [addr_grp.id]},
        ]

    def test_list_objects_brief(self):
        pass


class ServiceObjectAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the ServiceObject viewsets."""
    model = ServiceObject
    bulk_update_data = {"description": "test update description"}
    create_data = [
        {"name": "HTTP", "port": 80},
        {"name": "HTTP", "port": 8080},
    ]
    choices_fields = ["ip_protocol"]

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()

    def test_list_objects_brief(self):
        pass


class ServiceGroupAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the ServiceGroup viewsets."""
    model = ServiceObjectGroup
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        svc_obj = ServiceObject.objects.first()
        cls.create_data = [
            {"name": "test1", "service_objects": [svc_obj.id]},
            {"name": "test2", "service_objects": [svc_obj.id]},
        ]

    def test_list_objects_brief(self):
        pass


class ServicePolicyObjectAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the ServicePolicyObject viewsets."""
    model = ServicePolicyObject
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        svc_obj = ServiceObject.objects.first()
        svc_grp = ServiceObjectGroup.objects.first()
        cls.create_data = [
            {"name": "test1", "service_objects": [svc_obj.id]},
            {"name": "test2", "service_object_groups": [svc_grp.id]},
            {"name": "test3", "service_objects": [svc_obj.id], "service_object_groups": [svc_grp.id]},
        ]

    def test_list_objects_brief(self):
        pass


class UserObjectAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the User viewsets."""
    model = UserObject
    bulk_update_data = {"name": "User Name 123"}
    create_data = [
        {"username": "test1", "name": "Foo"},
        {"username": "test2", "name": "Bar"},
    ]

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()

    def test_list_objects_brief(self):
        pass


class UserObjectGroupAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the UserGroup viewsets."""
    model = UserObjectGroup
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        user = UserObject.objects.first()
        cls.create_data = [
            {"name": "test1", "user_objects": [user.id]},
            {"name": "test2", "user_objects": [user.id]},
        ]

    def test_list_objects_brief(self):
        pass


class UserPolicyObjectAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the UserPolicyObject viewsets."""
    model = UserPolicyObject
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        usr_obj = UserObject.objects.first()
        usr_grp = UserObjectGroup.objects.first()
        cls.create_data = [
            {"name": "test1", "user_objects": [usr_obj.id]},
            {"name": "test2", "user_object_groups": [usr_grp.id]},
            {"name": "test3", "user_objects": [usr_obj.id], "user_object_groups": [usr_grp.id]},
        ]

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
        create_env()

    def test_list_objects_brief(self):
        pass


class SourceAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the Source viewsets."""
    model = Source
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        svc = ServicePolicyObject.objects.first()
        usr = UserPolicyObject.objects.first()
        addr = AddressPolicyObject.objects.first()
        zone = Zone.objects.first()
        cls.create_data = [
            {"address": addr.id, "service": svc.id, "user": usr.id, "zone": zone.id},
            {"address": addr.id, "service": svc.id},
        ]

    def test_list_objects_brief(self):
        pass


class DestinationAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the Destination viewsets."""
    model = Destination
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        svc = ServicePolicyObject.objects.first()
        addr = AddressPolicyObject.objects.first()
        zone = Zone.objects.first()
        cls.create_data = [
            {"address": addr.id, "service": svc.id, "zone": zone.id},
            {"address": addr.id, "service": svc.id},
        ]

    def test_list_objects_brief(self):
        pass


class PolicyRuleAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the PolicyRule viewsets."""
    model = PolicyRule
    bulk_update_data = {"log": False}
    choices_fields = ["action"]

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        src = Source.objects.first()
        dest = Destination.objects.first()
        cls.create_data = [
            {"source": src.id, "destination": dest.id, "action": "Deny", "log": True, "index": 4, "name": "test rule"},
            {"source": src.id, "destination": dest.id, "action": "Deny", "log": False, "index": 5},
        ]

    def test_list_objects_brief(self):
        pass


class PolicyAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the Policy viewsets."""
    model = Policy
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        pol_rule = PolicyRule.objects.first()
        cls.create_data = [
            {"name": "test 1", "policy_rules": [pol_rule.id]},
            {"name": "test 2", "policy_rules": [pol_rule.id], "description": "Test desc"},
        ]

    def test_list_objects_brief(self):
        pass
