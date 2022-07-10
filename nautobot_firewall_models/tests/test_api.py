"""Unit tests for API views."""
# flake8: noqa: F403,405
from unittest import skip
from nautobot.utilities.testing import APIViewTestCases
from nautobot.ipam.models import Prefix

from nautobot_firewall_models import models
from .fixtures import create_env, create_ip_range, create_fqdn


class IPRangeAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the IPRange viewsets."""

    model = models.IPRange
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""

        cls.create_data = [
            {"start_address": "10.0.0.1", "end_address": "10.0.0.3"},
            {"start_address": "10.0.0.4", "end_address": "10.0.0.10"},
        ]
        create_ip_range()

    @skip("Not implemented")
    def test_list_objects_brief(self):
        pass


class FQDNAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the Protocol viewsets."""

    model = models.FQDN
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""

        cls.create_data = [
            {"name": "test.local"},
            {"name": "sub.test.local"},
        ]
        create_fqdn()

    @skip("Not implemented")
    def test_list_objects_brief(self):
        pass


class AddressObjectAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the AddressObject viewsets."""

    model = models.AddressObject
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        ip_range = models.IPRange.objects.first()
        prefix = Prefix.objects.first()

        cls.create_data = [
            {"name": "obj1", "ip_range": ip_range.id},
            {"name": "obj2", "prefix": prefix.id},
        ]

    @skip("Not implemented")
    def test_list_objects_brief(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects(self):
        pass


class AddressObjectGroupAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the AddressObjectGroup viewsets."""

    model = models.AddressObjectGroup
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        addr_obj = models.AddressObject.objects.first()

        cls.create_data = [
            {"name": "test1", "address_objects": [addr_obj.id]},
            {"name": "test2", "address_objects": [addr_obj.id]},
        ]

    @skip("Not implemented")
    def test_list_objects_brief(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects(self):
        pass

    def test_create_object(self):
        self.validation_excluded_fields = ["address_objects"]
        return super().test_create_object()

    def test_update_object(self):
        self.validation_excluded_fields = ["address_objects"]
        return super().test_update_object()

    def test_bulk_create_objects(self):
        self.validation_excluded_fields = ["address_objects"]
        return super().test_bulk_create_objects()


class ServiceObjectAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the ServiceObject viewsets."""

    model = models.ServiceObject
    bulk_update_data = {"description": "test update description"}
    choices_fields = ["ip_protocol"]

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""

        cls.create_data = [
            {"name": "HTTP", "port": "8088", "ip_protocol": "TCP"},
            {"name": "HTTP", "port": "8080-8088", "ip_protocol": "TCP"},
        ]
        create_env()

    @skip("Not implemented")
    def test_list_objects_brief(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects(self):
        pass


class ServiceGroupAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the ServiceGroup viewsets."""

    model = models.ServiceObjectGroup
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        svc_obj = models.ServiceObject.objects.first()

        cls.create_data = [
            {"name": "test1", "service_objects": [svc_obj.id]},
            {"name": "test2", "service_objects": [svc_obj.id]},
        ]

    @skip("Not implemented")
    def test_list_objects_brief(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects(self):
        pass

    def test_create_object(self):
        self.validation_excluded_fields = ["service_objects"]
        return super().test_create_object()

    def test_update_object(self):
        self.validation_excluded_fields = ["service_objects"]
        return super().test_update_object()

    def test_bulk_create_objects(self):
        self.validation_excluded_fields = ["service_objects"]
        return super().test_bulk_create_objects()


class UserObjectAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the User viewsets."""

    model = models.UserObject
    bulk_update_data = {"name": "User Name 123"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""

        cls.create_data = [
            {"username": "test1", "name": "Foo"},
            {"username": "test2", "name": "Bar"},
        ]
        create_env()

    @skip("Not implemented")
    def test_list_objects_brief(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects(self):
        pass


class UserObjectGroupAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the UserGroup viewsets."""

    model = models.UserObjectGroup
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        user = models.UserObject.objects.first()

        cls.create_data = [
            {"name": "test1", "user_objects": [user.id]},
            {"name": "test2", "user_objects": [user.id]},
        ]

    @skip("Not implemented")
    def test_list_objects_brief(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects(self):
        pass

    def test_create_object(self):
        self.validation_excluded_fields = ["user_objects"]
        return super().test_create_object()

    def test_update_object(self):
        self.validation_excluded_fields = ["user_objects"]
        return super().test_update_object()

    def test_bulk_create_objects(self):
        self.validation_excluded_fields = ["user_objects"]
        return super().test_bulk_create_objects()


class ZoneAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the Zone viewsets."""

    model = models.Zone
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""

        cls.create_data = [
            {"name": "trust"},
            {"name": "untrust"},
        ]
        create_env()

    @skip("Not implemented")
    def test_list_objects_brief(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects(self):
        pass


class PolicyRuleAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the PolicyRule viewsets."""

    model = models.PolicyRule
    bulk_update_data = {"log": False}
    choices_fields = ["action"]

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        src_usr = models.UserObject.objects.first()
        src_addr = models.AddressObject.objects.first()
        dest_addr = models.AddressObject.objects.last()

        svc = models.ServiceObject.objects.first()
        cls.create_data = [
            {
                # pylint: disable=R0801
                "source_user": [src_usr.id],
                "source_address": [src_addr.id],
                "destination_address": [dest_addr.id],
                "action": "deny",
                "log": True,
                "service": [svc.id],
                "name": "test rule",
            },
            {
                "source_user": [src_usr.id],
                "source_address": [src_addr.id],
                "destination_address": [dest_addr.id],
                "action": "deny",
                "log": False,
                "service": [svc.id],
                "name": "test rule",
            },
        ]

    def test_list_objects_brief(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_delete_object(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects(self):
        pass


class PolicyAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the Policy viewsets."""

    model = models.Policy
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        pol_rule = models.PolicyRule.objects.first()

        cls.create_data = [
            {"name": "test 1", "policy_rules": [{"rule": pol_rule.id}]},
            {"name": "test 2", "policy_rules": [{"rule": pol_rule.id}], "description": "Test desc"},
        ]

    @skip("Not implemented")
    def test_list_objects_brief(self):
        pass

    def test_create_object(self):
        self.validation_excluded_fields = ["policy_rules"]
        return super().test_create_object()

    def test_update_object(self):
        self.validation_excluded_fields = ["policy_rules"]
        return super().test_update_object()

    def test_bulk_create_objects(self):
        self.validation_excluded_fields = ["policy_rules"]
        return super().test_bulk_create_objects()

    @skip("on_delete set to PROTECT")
    def test_delete_object(self):
        pass

    @skip("on_delete set to PROTECT")
    def test_bulk_delete_objects(self):
        pass
