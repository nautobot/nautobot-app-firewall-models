"""Unit tests for API views."""
# flake8: noqa: F403,405
# pylint: disable=invalid-name
from nautobot.apps.testing import APIViewTestCases
from nautobot.dcim.models import Device
from nautobot.ipam.models import Prefix

from nautobot_firewall_models import models
from .fixtures import create_env, create_ip_range, create_fqdn


class IPRangeAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the IPRange viewsets."""

    model = models.IPRange
    brief_fields = ["display", "end_address", "id", "start_address", "url"]
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""

        cls.create_data = [
            {"start_address": "10.0.0.1", "end_address": "10.0.0.3"},
            {"start_address": "10.0.0.4", "end_address": "10.0.0.10"},
        ]
        create_ip_range()


class FQDNAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the Protocol viewsets."""

    model = models.FQDN
    brief_fields = ["display", "id", "name", "url"]
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""

        cls.create_data = [
            {"name": "test.local"},
            {"name": "sub.test.local"},
        ]
        create_fqdn()


class ApplicationObjectAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the ApplicationObject viewsets."""

    model = models.ApplicationObject
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        models.ApplicationObject.objects.create(name="deleteableobj1")
        models.ApplicationObject.objects.create(name="deleteableobj2")
        models.ApplicationObject.objects.create(name="deleteableobj3")
        cls.create_data = [
            {"name": "obj2", "risk": 1},
            {"name": "obj1", "risk": 1},
        ]


class ApplicationObjectGroupAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the ApplicationObjectGroup viewsets."""

    model = models.ApplicationObjectGroup
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        app_obj = models.ApplicationObject.objects.first()
        models.ApplicationObjectGroup.objects.create(name="deleteableobj1")
        models.ApplicationObjectGroup.objects.create(name="deleteableobj2")
        models.ApplicationObjectGroup.objects.create(name="deleteableobj3")

        cls.create_data = [
            {"name": "test1", "application_objects": [app_obj.id]},
            {"name": "test2", "application_objects": [app_obj.id]},
        ]


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
        models.AddressObject.objects.create(name="deleteableobj1", prefix=prefix)
        models.AddressObject.objects.create(name="deleteableobj2", prefix=prefix)
        models.AddressObject.objects.create(name="deleteableobj3", prefix=prefix)

        cls.create_data = [
            {"name": "obj2", "prefix": prefix.id},
            {"name": "obj1", "ip_range": ip_range.id},
        ]


class AddressObjectGroupAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the AddressObjectGroup viewsets."""

    model = models.AddressObjectGroup
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        addr_obj = models.AddressObject.objects.first()
        models.AddressObjectGroup.objects.create(name="deleteableobj1")
        models.AddressObjectGroup.objects.create(name="deleteableobj2")
        models.AddressObjectGroup.objects.create(name="deleteableobj3")

        cls.create_data = [
            {"name": "test1", "address_objects": [addr_obj.id]},
            {"name": "test2", "address_objects": [addr_obj.id]},
        ]


class ServiceObjectAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the ServiceObject viewsets."""

    model = models.ServiceObject
    bulk_update_data = {"description": "test update description"}
    choices_fields = ["ip_protocol"]

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        models.ServiceObject.objects.create(name="deleteableobj1", ip_protocol="TCP")
        models.ServiceObject.objects.create(name="deleteableobj2", ip_protocol="TCP")
        models.ServiceObject.objects.create(name="deleteableobj3", ip_protocol="TCP")

        cls.create_data = [
            {"name": "HTTP", "port": "8088", "ip_protocol": "TCP"},
            {"name": "HTTP", "port": "8080-8088", "ip_protocol": "TCP"},
        ]
        create_env()


class ServiceGroupAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the ServiceGroup viewsets."""

    model = models.ServiceObjectGroup
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        svc_obj = models.ServiceObject.objects.first()
        models.ServiceObjectGroup.objects.create(name="deleteableobj1")
        models.ServiceObjectGroup.objects.create(name="deleteableobj2")
        models.ServiceObjectGroup.objects.create(name="deleteableobj3")

        cls.create_data = [
            {"name": "test1", "service_objects": [svc_obj.id]},
            {"name": "test2", "service_objects": [svc_obj.id]},
        ]


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
        models.UserObject.objects.create(username="deleteableobj1", name="deleteableobj1")
        models.UserObject.objects.create(username="deleteableobj2", name="deleteableobj2")
        models.UserObject.objects.create(username="deleteableobj3", name="deleteableobj3")
        create_env()


class UserObjectGroupAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the UserGroup viewsets."""

    model = models.UserObjectGroup
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        user = models.UserObject.objects.first()
        models.UserObjectGroup.objects.create(name="deleteableobj1")
        models.UserObjectGroup.objects.create(name="deleteableobj2")
        models.UserObjectGroup.objects.create(name="deleteableobj3")

        cls.create_data = [
            {"name": "test1", "user_objects": [user.id]},
            {"name": "test2", "user_objects": [user.id]},
        ]


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
        models.Zone.objects.create(name="deleteableobj1")
        models.Zone.objects.create(name="deleteableobj2")
        models.Zone.objects.create(name="deleteableobj3")
        create_env()


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
        models.PolicyRule.objects.create(name="deleteableobj1", action="deny", index=1)
        models.PolicyRule.objects.create(name="deleteableobj2", action="deny", index=1)
        models.PolicyRule.objects.create(name="deleteableobj3", action="deny", index=1)
        cls.create_data = [
            {
                # pylint: disable=R0801
                "source_users": [src_usr.id],
                "source_addresses": [src_addr.id],
                "destination_addresses": [dest_addr.id],
                "action": "deny",
                "log": True,
                "destination_services": [svc.id],
                "name": "test rule 1",
            },
            {
                "source_users": [src_usr.id],
                "source_addresses": [src_addr.id],
                "destination_addresses": [dest_addr.id],
                "action": "deny",
                "log": False,
                "destination_services": [svc.id],
                "name": "test rule 2",
            },
        ]


class PolicyAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the Policy viewsets."""

    model = models.Policy
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        pol_rule = models.PolicyRule.objects.first()
        dev = Device.objects.first()
        models.Policy.objects.create(name="deleteableobj1")
        models.Policy.objects.create(name="deleteableobj2")
        models.Policy.objects.create(name="deleteableobj3")

        cls.create_data = [
            {"name": "test 1", "policy_rules": [pol_rule.id]},
            {"name": "test 2", "policy_rules": [pol_rule.id], "description": "Test desc", "assigned_devices": [dev.id]},
        ]


class NATPolicyRuleAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the PolicyRule viewsets."""

    model = models.NATPolicyRule
    bulk_update_data = {"log": False}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        src_addr = models.AddressObject.objects.first()
        dest_addr = models.AddressObject.objects.last()
        svc = models.ServiceObject.objects.first()
        models.NATPolicyRule.objects.create(name="deleteableobj1")
        models.NATPolicyRule.objects.create(name="deleteableobj2")
        models.NATPolicyRule.objects.create(name="deleteableobj3")
        cls.create_data = [
            {
                "original_source_addresses": [src_addr.id],
                "original_destination_addresses": [dest_addr.id],
                "translated_destination_addresses": [src_addr.id],
                "log": True,
                "original_destination_services": [svc.id],
                "name": "test rule",
            },
            {
                "original_source_addresses": [src_addr.id],
                "original_destination_addresses": [dest_addr.id],
                "translated_destination_addresses": [src_addr.id],
                "log": False,
                "original_destination_services": [svc.id],
                "name": "test rule",
            },
        ]


class NATPolicyAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the Policy viewsets."""

    model = models.NATPolicy
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        create_env()
        nat_pol_rule = models.NATPolicyRule.objects.first()
        models.NATPolicy.objects.create(name="deleteableobj1")
        models.NATPolicy.objects.create(name="deleteableobj2")
        models.NATPolicy.objects.create(name="deleteableobj3")

        cls.create_data = [
            {"name": "test 1", "nat_policy_rules": [nat_pol_rule.id]},
            {"name": "test 2", "nat_policy_rules": [nat_pol_rule.id], "description": "Test desc"},
        ]
