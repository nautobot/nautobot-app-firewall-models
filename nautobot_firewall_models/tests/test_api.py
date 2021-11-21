"""Unit tests for API views."""
# flake8: noqa: F403,405
from nautobot.extras.models.statuses import Status
from nautobot.utilities.testing import APIViewTestCases
from nautobot.ipam.models import Prefix

from nautobot_firewall_models.models import *  # pylint: disable=unused-wildcard-import, wildcard-import
from .fixtures import create_env, create_ip_range, create_fqdn


class IPRangeAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the IPRange viewsets."""
    model = IPRange
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        status = Status.objects.get(slug="active").id
        cls.create_data = [
            {"start_address": "10.0.0.1", "end_address": "10.0.0.3", "status": status},
            {"start_address": "10.0.0.4", "end_address": "10.0.0.10", "status": status},
        ]
        create_ip_range()

    def test_list_objects_brief(self):
        pass


class FQDNAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the Protocol viewsets."""
    model = FQDN
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        status = Status.objects.get(slug="active").id
        cls.create_data = [
            {"name": "test.local", "status": status},
            {"name": "sub.test.local", "status": status},
        ]
        create_fqdn()

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
        status = Status.objects.get(slug="active").id

        cls.create_data = [
            {"name": "obj1", "ip_range": ip_range.id, "status": status},
            {"name": "obj2", "prefix": prefix.id, "status": status},
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
        status = Status.objects.get(slug="active").id
        cls.create_data = [
            {"name": "test1", "address_objects": [addr_obj.id], "status": status},
            {"name": "test2", "address_objects": [addr_obj.id], "status": status},
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
        status = Status.objects.get(slug="active").id
        addr_obj = AddressObject.objects.first()
        addr_grp = AddressObjectGroup.objects.first()
        cls.create_data = [
            {"name": "test1", "address_objects": [addr_obj.id], "status": status},
            {"name": "test2", "address_object_groups": [addr_grp.id], "status": status},
            {
                "name": "test3",
                "address_objects": [addr_obj.id],
                "address_object_groups": [addr_grp.id],
                "status": status,
            },
        ]

    def test_list_objects_brief(self):
        pass


class ServiceObjectAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the ServiceObject viewsets."""
    model = ServiceObject
    bulk_update_data = {"description": "test update description"}
    choices_fields = ["ip_protocol"]

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        status = Status.objects.get(slug="active").id
        cls.create_data = [
            {"name": "HTTP", "port": 80, "status": status},
            {"name": "HTTP", "port": 8080, "status": status},
        ]
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
        status = Status.objects.get(slug="active").id
        cls.create_data = [
            {"name": "test1", "service_objects": [svc_obj.id], "status": status},
            {"name": "test2", "service_objects": [svc_obj.id], "status": status},
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
        status = Status.objects.get(slug="active").id
        svc_obj = ServiceObject.objects.first()
        svc_grp = ServiceObjectGroup.objects.first()
        cls.create_data = [
            {"name": "test1", "service_objects": [svc_obj.id], "status": status},
            {"name": "test2", "service_object_groups": [svc_grp.id], "status": status},
            {"name": "test3", "service_objects": [svc_obj.id], "service_object_groups": [svc_grp.id], "status": status},
        ]

    def test_list_objects_brief(self):
        pass


class UserObjectAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the User viewsets."""
    model = UserObject
    bulk_update_data = {"name": "User Name 123"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        status = Status.objects.get(slug="active").id
        cls.create_data = [
            {"username": "test1", "name": "Foo", "status": status},
            {"username": "test2", "name": "Bar", "status": status},
        ]
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
        status = Status.objects.get(slug="active").id
        cls.create_data = [
            {"name": "test1", "user_objects": [user.id], "status": status},
            {"name": "test2", "user_objects": [user.id], "status": status},
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
        status = Status.objects.get(slug="active").id
        usr_obj = UserObject.objects.first()
        usr_grp = UserObjectGroup.objects.first()
        cls.create_data = [
            {"name": "test1", "user_objects": [usr_obj.id], "status": status},
            {"name": "test2", "user_object_groups": [usr_grp.id], "status": status},
            {"name": "test3", "user_objects": [usr_obj.id], "user_object_groups": [usr_grp.id], "status": status},
        ]

    def test_list_objects_brief(self):
        pass


class ZoneAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the Zone viewsets."""
    model = Zone
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        status = Status.objects.get(slug="active").id
        cls.create_data = [
            {"name": "trust", "status": status},
            {"name": "untrust", "status": status},
        ]
        create_env()

    def test_list_objects_brief(self):
        pass


class SourceDestinationAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=R0901
    """Test the Source viewsets."""
    model = SourceDestination
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        svc = ServicePolicyObject.objects.first()
        usr = UserPolicyObject.objects.first()
        addr = AddressPolicyObject.objects.first()
        zone = Zone.objects.first()
        status = Status.objects.get(slug="active").id
        cls.create_data = [
            {"address": addr.id, "service": svc.id, "user": usr.id, "zone": zone.id, "status": status},
            {"address": addr.id, "service": svc.id, "status": status},
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
        src = SourceDestination.objects.first()
        dest = SourceDestination.objects.last()
        status = Status.objects.get(slug="active").id
        cls.create_data = [
            {"source": src.id, "destination": dest.id, "action": "Deny", "log": True, "index": 4, "status": status},
            {"source": src.id, "destination": dest.id, "action": "Deny", "log": False, "index": 5, "status": status},
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
        status = Status.objects.get(slug="active").id
        cls.create_data = [
            {"name": "test 1", "policy_rules": [pol_rule.id], "status": status},
            {"name": "test 2", "policy_rules": [pol_rule.id], "description": "Test desc", "status": status},
        ]

    def test_list_objects_brief(self):
        pass
