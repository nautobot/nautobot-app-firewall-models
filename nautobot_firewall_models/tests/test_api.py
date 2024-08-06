"""Unit tests for API views."""

# flake8: noqa: F403,405
# pylint: disable=invalid-name
# pylint: disable=duplicate-code
from django.contrib.contenttypes.models import ContentType
from nautobot.apps.testing import APIViewTestCases, disable_warnings
from nautobot.dcim.models import Location, Platform, DeviceType, Device
from nautobot.extras.models import Status, Role
from nautobot.ipam.models import Prefix, VRF
from nautobot.users.models import ObjectPermission
from rest_framework import status

from nautobot_firewall_models import models
from . import fixtures


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
        fixtures.create_ip_range()

    def test_unique_validators(self):
        """Test the unique validators for IPRange."""
        # Add object-level permission
        obj_perm = ObjectPermission(name="Test permission", actions=["add"])
        obj_perm.save()
        obj_perm.users.add(self.user)
        obj_perm.object_types.add(ContentType.objects.get_for_model(self.model))

        vrfs = (
            VRF.objects.create(name="test vrf 1"),
            VRF.objects.create(name="test vrf 2"),
        )

        url = self._get_list_url()

        # Create an IPRange object with a vrf
        models.IPRange.objects.create(start_address="1.0.0.1", end_address="1.0.0.8", vrf=vrfs[0])

        initial_count = self._get_queryset().count()

        # Create an IPRange object with the same start and end address but a different vrf
        with disable_warnings("django.request"):
            data = {"start_address": "1.0.0.1", "end_address": "1.0.0.8", "vrf": vrfs[1].pk}
            response = self.client.post(url, data, format="json", **self.header)
            self.assertHttpStatus(response, status.HTTP_201_CREATED)
            self.assertEqual(self._get_queryset().count(), initial_count + 1)

        # Creating an IPRange object with the same start and end address and the same vrf fails
        with disable_warnings("django.request"):
            data = {"start_address": "1.0.0.1", "end_address": "1.0.0.8", "vrf": vrfs[0].pk}
            response = self.client.post(url, data, format="json", **self.header)
            self.assertHttpStatus(response, status.HTTP_400_BAD_REQUEST)
            self.assertIn("non_field_errors", response.data)
            self.assertEqual(
                "The fields start_address, end_address, vrf must make a unique set.",
                response.data["non_field_errors"][0],
            )
            self.assertEqual(self._get_queryset().count(), initial_count + 1)

        # Create another IPRange object with no vrf
        models.IPRange.objects.create(start_address="2.0.0.1", end_address="2.0.0.8")

        # Creating an IPRange object with the same start and end address with no vrf fails
        with disable_warnings("django.request"):
            data = {"start_address": "2.0.0.1", "end_address": "2.0.0.8"}
            response = self.client.post(url, data, format="json", **self.header)
            self.assertHttpStatus(response, status.HTTP_400_BAD_REQUEST)
            self.assertIn("non_field_errors", response.data)
            self.assertEqual(
                "The fields start_address, end_address must make a unique set.",
                response.data["non_field_errors"][0],
            )
            self.assertEqual(self._get_queryset().count(), initial_count + 2)

        # Create an IPRange object with the same start and end address with a vrf
        with disable_warnings("django.request"):
            data = {"start_address": "2.0.0.1", "end_address": "2.0.0.8", "vrf": vrfs[0].pk}
            response = self.client.post(url, data, format="json", **self.header)
            self.assertHttpStatus(response, status.HTTP_201_CREATED)
            self.assertEqual(self._get_queryset().count(), initial_count + 3)


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
        fixtures.create_fqdn()


class ApplicationObjectAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the ApplicationObject viewsets."""

    model = models.ApplicationObject
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        fixtures.create_app_obj()
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
        fixtures.create_app_group()
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
        fixtures.create_addr_obj()
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
        fixtures.create_addr_group()
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
        fixtures.create_svc_obj()


class ServiceGroupAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the ServiceGroup viewsets."""

    model = models.ServiceObjectGroup
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        fixtures.create_svc_group()
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
        fixtures.create_user_obj()


class UserObjectGroupAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the UserGroup viewsets."""

    model = models.UserObjectGroup
    bulk_update_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        fixtures.create_user_group()
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
        fixtures.create_zone()


class PolicyRuleAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the PolicyRule viewsets."""

    model = models.PolicyRule
    bulk_update_data = {"log": False}
    choices_fields = ["action"]

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        fixtures.create_policy_rule()
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
        fixtures.create_policy()
        pol_rule = models.PolicyRule.objects.first()
        models.Policy.objects.create(name="deleteableobj1")
        models.Policy.objects.create(name="deleteableobj2")
        models.Policy.objects.create(name="deleteableobj3")

        cls.create_data = [
            {"name": "test 1", "policy_rules": [pol_rule.id]},
            {"name": "test 2", "policy_rules": [pol_rule.id], "description": "Test desc"},
        ]


class NATPolicyRuleAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the PolicyRule viewsets."""

    model = models.NATPolicyRule
    bulk_update_data = {"log": False}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        fixtures.create_natpolicy_rule()
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
        fixtures.create_natpolicy()
        nat_pol_rule = models.NATPolicyRule.objects.first()
        models.NATPolicy.objects.create(name="deleteableobj1")
        models.NATPolicy.objects.create(name="deleteableobj2")
        models.NATPolicy.objects.create(name="deleteableobj3")

        cls.create_data = [
            {"name": "test 1", "nat_policy_rules": [nat_pol_rule.id]},
            {"name": "test 2", "nat_policy_rules": [nat_pol_rule.id], "description": "Test desc"},
        ]


###########################
# Through Models
###########################
class PolicyDeviceM2MAPIViewTest(APIViewTestCases.APIViewTestCase):
    """Test the PolicyDeviceM2M viewsets."""

    model = models.PolicyDeviceM2M
    bulk_update_data = {"weight": 1000}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        fixtures.assign_policies()
        policy = models.Policy.objects.first()
        location = Location.objects.get(name="DFW02")
        dev_role = Role.objects.get(name="WAN")
        status = Status.objects.get(name="Active")
        platform = Platform.objects.get(name="Juniper")
        dev_type = DeviceType.objects.get(model="SRX300")
        dev1 = Device.objects.create(
            name="TEST-DEV-01",
            role=dev_role,
            device_type=dev_type,
            location=location,
            status=status,
            platform=platform,
        )
        dev2 = Device.objects.create(
            name="TEST-DEV-02",
            role=dev_role,
            device_type=dev_type,
            location=location,
            status=status,
            platform=platform,
        )

        cls.create_data = [
            {"device": dev1.id, "policy": policy.id, "weight": 100},
            {"device": dev2.id, "policy": policy.id, "weight": 200},
        ]
