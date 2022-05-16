"""Unit tests for views."""
# flake8: noqa: F403,405
from unittest import skip
from nautobot.extras.models.statuses import Status
from nautobot.utilities.testing import ViewTestCases

from nautobot_firewall_models.models import *  # pylint: disable=unused-wildcard-import, wildcard-import
from .fixtures import create_env, create_fqdn, create_ip_range


class IPRangeUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the IPRange viewsets."""
    model = IPRange
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for UI calls."""
        status = Status.objects.get(slug="active").id
        cls.form_data = {"start_address": "10.0.0.1", "end_address": "10.0.0.3", "status": status}
        create_ip_range()

    @skip("Not implemented")
    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_without_permission(self):
        pass


class FQDNUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the Protocol viewsets."""
    model = FQDN
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        status = Status.objects.get(slug="active").id
        cls.form_data = {"name": "test.local", "status": status}
        create_fqdn()

    @skip("Not implemented")
    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_without_permission(self):
        pass


class AddressObjectUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the AddressObject viewsets."""
    model = AddressObject
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        ip_range = IPRange.objects.first()
        status = Status.objects.get(slug="active").id

        cls.form_data = {"name": "obj1", "ip_range": ip_range.id, "status": status}

    @skip("Not implemented")
    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_without_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects_with_constrained_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects_with_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object_with_constrained_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object_with_permission(self):
        pass


class AddressObjectGroupUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the AddressObjectGroup viewsets."""
    model = AddressObjectGroup
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        status = Status.objects.get(slug="active").id
        addr_obj = AddressObject.objects.first()
        cls.form_data = {"name": "test1", "address_objects": [addr_obj.id], "status": status}

    @skip("Not implemented")
    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_without_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects_with_constrained_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects_with_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object_with_constrained_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object_with_permission(self):
        pass


class ServiceObjectUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the ServiceObject viewsets."""
    model = ServiceObject
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        status = Status.objects.get(slug="active").id
        cls.form_data = {"name": "HTTP", "port": "8088", "status": status, "ip_protocol": "TCP"}
        create_env()

    @skip("Not implemented")
    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_without_permission(self):
        pass

    def test_service_object_str(self):
        """testing str of service object."""
        svc = ServiceObject.objects.first()
        svc.ip_protocol = "TCP"

        self.assertEqual(str(svc), svc.name)

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects_with_constrained_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects_with_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object_with_constrained_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object_with_permission(self):
        pass


class ServiceGroupUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the ServiceGroup viewsets."""
    model = ServiceObjectGroup
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        svc_obj = ServiceObject.objects.first()
        status = Status.objects.get(slug="active").id
        cls.form_data = {"name": "test1", "service_objects": [svc_obj.id], "status": status}

    @skip("Not implemented")
    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_without_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects_with_constrained_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects_with_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object_with_constrained_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object_with_permission(self):
        pass


class UserObjectUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the User viewsets."""
    model = UserObject
    bulk_edit_data = {"name": "User Name 123"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        status = Status.objects.get(slug="active").id
        cls.form_data = {"username": "test1", "name": "Foo", "status": status}
        create_env()

    @skip("Not implemented")
    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_without_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects_with_constrained_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects_with_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object_with_constrained_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object_with_permission(self):
        pass


class UserObjectGroupUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the UserGroup viewsets."""
    model = UserObjectGroup
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        user = UserObject.objects.first()
        status = Status.objects.get(slug="active").id
        cls.form_data = {"name": "test1", "user_objects": [user.id], "status": status}

    @skip("Not implemented")
    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_without_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects_with_constrained_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects_with_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object_with_constrained_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object_with_permission(self):
        pass


class ZoneUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the Zone viewsets."""
    model = Zone
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for UI calls."""
        status = Status.objects.get(slug="active").id
        cls.form_data = {"name": "trust", "status": status}
        create_env()

    @skip("Not implemented")
    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_without_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects_with_constrained_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects_with_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object_with_constrained_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object_with_permission(self):
        pass


class PolicyRuleUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the PolicyRule viewsets."""
    model = PolicyRule
    bulk_edit_data = {"log": True}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        src_usr = UserObject.objects.first()
        src_addr = AddressObject.objects.first()
        dest_addr = AddressObject.objects.last()
        status = Status.objects.get(slug="active").id
        svc = ServiceObject.objects.first()
        cls.form_data = {
            # pylint: disable=R0801
            "source_user": [src_usr.id],
            "source_address": [src_addr.id],
            "destination_address": [dest_addr.id],
            "action": "deny",
            "log": True,
            "service": [svc.id],
            "name": "test rule",
            "status": status,
        }

    @skip("Not implemented")
    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_without_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects_with_constrained_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects_with_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object_with_constrained_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object_with_permission(self):
        pass


class PolicyUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=R0901
    """Test the Policy viewsets."""
    model = Policy
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        pol_rule = PolicyRule.objects.first()
        status = Status.objects.get(slug="active").id
        cls.form_data = {
            "name": "test 2",
            "policy_rules": [pol_rule.id],
            "description": "Test desc",
            "status": status,
        }

    @skip("Not implemented")
    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_without_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects_with_constrained_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects_with_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object_with_constrained_permission(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object_with_permission(self):
        pass
