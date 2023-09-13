"""Unit tests for views."""
# flake8: noqa: F403,405
# pylint: disable=invalid-name
from unittest import skip
from nautobot.extras.models.statuses import Status
from nautobot.apps.testing import ViewTestCases

from nautobot_firewall_models.models import *  # pylint: disable=unused-wildcard-import, wildcard-import
from .fixtures import create_env, create_fqdn, create_ip_range


class IPRangeUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the IPRange viewsets."""

    model = IPRange
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for UI calls."""
        status = Status.objects.get(name="Active").id
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

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission_csv_file(self):
        pass


class FQDNUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the Protocol viewsets."""

    model = FQDN
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        status = Status.objects.get(name="Active").id
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

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission_csv_file(self):
        pass


class AddressObjectUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the AddressObject viewsets."""

    model = AddressObject
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        ip_range = IPRange.objects.first()
        status = Status.objects.get(name="Active").id
        AddressObject.objects.create(name="deleteableobj1", ip_range=ip_range)
        AddressObject.objects.create(name="deleteableobj2", ip_range=ip_range)
        AddressObject.objects.create(name="deleteableobj3", ip_range=ip_range)

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

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission_csv_file(self):
        pass


class AddressObjectGroupUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the AddressObjectGroup viewsets."""

    model = AddressObjectGroup
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        status = Status.objects.get(name="Active").id
        addr_obj = AddressObject.objects.first()
        AddressObjectGroup.objects.create(name="deleteableobj1")
        AddressObjectGroup.objects.create(name="deleteableobj2")
        AddressObjectGroup.objects.create(name="deleteableobj3")
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

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission_csv_file(self):
        pass


class ApplicationObjectUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the ApplicationObject viewsets."""

    model = ApplicationObject
    bulk_edit_data = {"description": "bulk test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        ApplicationObject.objects.create(name="deleteableobj1")
        ApplicationObject.objects.create(name="deleteableobj2")
        ApplicationObject.objects.create(name="deleteableobj3")
        status = Status.objects.get(name="Active").id
        cls.form_data = {"name": "obj1", "risk": 1, "status": status}

    @skip("Not implemented")
    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_without_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission_csv_file(self):
        pass


class ApplicationObjectGroupUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the ApplicationObjectGroup viewsets."""

    model = ApplicationObjectGroup
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        status = Status.objects.get(name="Active").id
        app_obj = ApplicationObject.objects.first()
        ApplicationObjectGroup.objects.create(name="deleteableobj1")
        ApplicationObjectGroup.objects.create(name="deleteableobj2")
        ApplicationObjectGroup.objects.create(name="deleteableobj3")
        cls.form_data = {"name": "test1", "application_objects": [app_obj.id], "status": status}

    @skip("Not implemented")
    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_without_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission_csv_file(self):
        pass


class ServiceObjectUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the ServiceObject viewsets."""

    model = ServiceObject
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        ServiceObject.objects.create(name="deleteableobj1", ip_protocol="TCP")
        ServiceObject.objects.create(name="deleteableobj2", ip_protocol="TCP")
        ServiceObject.objects.create(name="deleteableobj3", ip_protocol="TCP")
        status = Status.objects.get(name="Active").id
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

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission_csv_file(self):
        pass


class ServiceGroupUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the ServiceGroup viewsets."""

    model = ServiceObjectGroup
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        svc_obj = ServiceObject.objects.first()
        status = Status.objects.get(name="Active").id
        ServiceObjectGroup.objects.create(name="deleteableobj1")
        ServiceObjectGroup.objects.create(name="deleteableobj2")
        ServiceObjectGroup.objects.create(name="deleteableobj3")
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

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission_csv_file(self):
        pass


class UserObjectUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the User viewsets."""

    model = UserObject
    bulk_edit_data = {"name": "User Name 123"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        status = Status.objects.get(name="Active").id
        UserObject.objects.create(username="deleteableobj1", name="deleteableobj1")
        UserObject.objects.create(username="deleteableobj2", name="deleteableobj2")
        UserObject.objects.create(username="deleteableobj3", name="deleteableobj3")
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

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission_csv_file(self):
        pass


class UserObjectGroupUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the UserGroup viewsets."""

    model = UserObjectGroup
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        user = UserObject.objects.first()
        status = Status.objects.get(name="Active").id
        UserObjectGroup.objects.create(name="deleteableobj1")
        UserObjectGroup.objects.create(name="deleteableobj2")
        UserObjectGroup.objects.create(name="deleteableobj3")
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

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission_csv_file(self):
        pass


class ZoneUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the Zone viewsets."""

    model = Zone
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for UI calls."""
        status = Status.objects.get(name="Active").id
        Zone.objects.create(name="deleteableobj1")
        Zone.objects.create(name="deleteableobj2")
        Zone.objects.create(name="deleteableobj3")
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

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission_csv_file(self):
        pass


class PolicyRuleUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the PolicyRule viewsets."""

    model = PolicyRule
    bulk_edit_data = {"description": "bulk test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        src_usr = UserObject.objects.first()
        src_addr = AddressObject.objects.first()
        dest_addr = AddressObject.objects.last()
        status = Status.objects.get(name="Active").id
        svc = ServiceObject.objects.first()
        PolicyRule.objects.create(name="deleteableobj1", action="deny", index=1)
        PolicyRule.objects.create(name="deleteableobj2", action="deny", index=1)
        PolicyRule.objects.create(name="deleteableobj3", action="deny", index=1)
        cls.form_data = {
            # pylint: disable=R0801
            "source_users": [src_usr.id],
            "source_addresses": [src_addr.id],
            "destination_addresses": [dest_addr.id],
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

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission_csv_file(self):
        pass


class PolicyUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the Policy viewsets."""

    model = Policy
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        pol_rule = PolicyRule.objects.first()
        status = Status.objects.get(name="Active").id
        Policy.objects.create(name="deleteableobj1")
        Policy.objects.create(name="deleteableobj2")
        Policy.objects.create(name="deleteableobj3")
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

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission_csv_file(self):
        pass


class NATPolicyRuleUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the Policy viewsets."""

    model = NATPolicyRule
    bulk_edit_data = {"log": False}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        src_addr = AddressObject.objects.first()
        dest_addr = AddressObject.objects.last()
        svc = ServiceObject.objects.first()
        status = Status.objects.get(name="Active").id
        NATPolicyRule.objects.create(name="deleteableobj1")
        NATPolicyRule.objects.create(name="deleteableobj2")
        NATPolicyRule.objects.create(name="deleteableobj3")
        cls.form_data = {
            "original_source_addresses": [src_addr.id],
            "original_destination_addresses": [dest_addr.id],
            "translated_destination_addresses": [src_addr.id],
            "log": True,
            "original_destination_services": [svc.id],
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

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission_csv_file(self):
        pass


class NATPolicyUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the Policy viewsets."""

    model = NATPolicy
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        status = Status.objects.get(name="Active").id
        nat_pol_rule = NATPolicyRule.objects.first()
        NATPolicy.objects.create(name="deleteableobj1")
        NATPolicy.objects.create(name="deleteableobj2")
        NATPolicy.objects.create(name="deleteableobj3")
        cls.form_data = {"status": status, "name": "test 1", "nat_policy_rules": [nat_pol_rule.id]}

    @skip("Not implemented")
    def test_bulk_import_objects_with_constrained_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_without_permission(self):
        pass

    @skip("Not implemented")
    def test_bulk_import_objects_with_permission_csv_file(self):
        pass
