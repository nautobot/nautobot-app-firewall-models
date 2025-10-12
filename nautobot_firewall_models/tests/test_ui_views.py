"""Unit tests for views."""

# ruff: noqa: F403, F405
# pylint: disable=invalid-name
# pylint: disable=duplicate-code
from nautobot.apps.testing import ViewTestCases
from nautobot.dcim.models import Device
from nautobot.extras.models.statuses import Status

from nautobot_firewall_models.models import *  # pylint: disable=unused-wildcard-import, wildcard-import

from . import fixtures


class IPRangeUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the IPRange viewsets."""

    model = IPRange
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for UI calls."""
        status = Status.objects.get(name="Active").id
        cls.form_data = {"start_address": "10.0.0.1", "end_address": "10.0.0.3", "status": status}
        fixtures.create_ip_range()
        cls.csv_data = (
            "start_address,end_address,status",
            "11.11.11.1,11.11.11.11,Active",
            "11.11.21.1,11.11.21.11,Active",
            "11.11.31.1,11.11.31.11,Active",
        )


class FQDNUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the Protocol viewsets."""

    model = FQDN
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        status = Status.objects.get(name="Active").id
        cls.form_data = {"name": "test.local", "status": status}
        fixtures.create_fqdn()
        cls.csv_data = (
            "name,status",
            "foo.bar.com,Active",
            "bar.foo.com,Active",
            "bar.baz.foo.com,Active",
        )


class AddressObjectUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the AddressObject viewsets."""

    model = AddressObject
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        fixtures.create_addr_obj()
        ip_range = IPRange.objects.first()
        status = Status.objects.get(name="Active").id
        AddressObject.objects.create(name="deleteableobj1", ip_range=ip_range)
        AddressObject.objects.create(name="deleteableobj2", ip_range=ip_range)
        AddressObject.objects.create(name="deleteableobj3", ip_range=ip_range)

        cls.form_data = {"name": "obj1", "ip_range": ip_range.id, "status": status}
        cls.csv_data = (
            "name,ip_range,status",
            f"csvobj1,{ip_range.id},Active",
            f"csvobj2,{ip_range.id},Active",
            f"csvobj3,{ip_range.id},Active",
        )


class AddressObjectGroupUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the AddressObjectGroup viewsets."""

    model = AddressObjectGroup
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        fixtures.create_addr_group()
        status = Status.objects.get(name="Active").id
        addr_obj = AddressObject.objects.first()
        AddressObjectGroup.objects.create(name="deleteableobj1")
        AddressObjectGroup.objects.create(name="deleteableobj2")
        AddressObjectGroup.objects.create(name="deleteableobj3")
        cls.form_data = {"name": "test1", "address_objects": [addr_obj.id], "status": status}
        cls.csv_data = (
            "name,address_objects,status",
            f'csvobj1,"{addr_obj.id}",Active',
            f'csvobj2,"{addr_obj.id}",Active',
            f'csvobj3,"{addr_obj.id}",Active',
        )


class ApplicationObjectUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the ApplicationObject viewsets."""

    model = ApplicationObject
    bulk_edit_data = {"description": "bulk test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        fixtures.create_app_obj()
        ApplicationObject.objects.create(name="deleteableobj1")
        ApplicationObject.objects.create(name="deleteableobj2")
        ApplicationObject.objects.create(name="deleteableobj3")
        status = Status.objects.get(name="Active").id
        cls.form_data = {"name": "obj1", "risk": 1, "status": status}
        cls.csv_data = (
            "name,risk,status",
            "csvobj1,1,Active",
            "csvobj2,2,Active",
            "csvobj3,3,Active",
        )


class ApplicationObjectGroupUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the ApplicationObjectGroup viewsets."""

    model = ApplicationObjectGroup
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        fixtures.create_app_group()
        status = Status.objects.get(name="Active").id
        app_obj = ApplicationObject.objects.first()
        ApplicationObjectGroup.objects.create(name="deleteableobj1")
        ApplicationObjectGroup.objects.create(name="deleteableobj2")
        ApplicationObjectGroup.objects.create(name="deleteableobj3")
        cls.form_data = {"name": "test1", "application_objects": [app_obj.id], "status": status}
        cls.csv_data = (
            "name,application_objects,status",
            f'csvobj1,"{app_obj.id}",Active',
            f'csvobj2,"{app_obj.id}",Active',
            f'csvobj3,"{app_obj.id}",Active',
        )


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
        fixtures.create_svc_obj()
        cls.csv_data = (
            "name,port,ip_protocol,status",
            "csvobj1,1,TCP,Active",
            "csvobj2,2,TCP,Active",
            "csvobj3,3,TCP,Active",
        )


class ServiceObjectGroupUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the ServiceGroup viewsets."""

    model = ServiceObjectGroup
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        fixtures.create_svc_group()
        svc_obj = ServiceObject.objects.first()
        status = Status.objects.get(name="Active").id
        ServiceObjectGroup.objects.create(name="deleteableobj1")
        ServiceObjectGroup.objects.create(name="deleteableobj2")
        ServiceObjectGroup.objects.create(name="deleteableobj3")
        cls.form_data = {"name": "test1", "service_objects": [svc_obj.id], "status": status}
        cls.csv_data = (
            "name,service_objects,status",
            f'csvobj1,"{svc_obj.id}",Active',
            f'csvobj2,"{svc_obj.id}",Active',
            f'csvobj3,"{svc_obj.id}",Active',
        )


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
        fixtures.create_user_obj()
        cls.csv_data = (
            "name,username,status",
            "csvobj1,csvuser1,Active",
            "csvobj2,csvuser2,Active",
            "csvobj3,csvuser3,Active",
        )


class UserObjectGroupUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the UserGroup viewsets."""

    model = UserObjectGroup
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        fixtures.create_user_group()
        user = UserObject.objects.first()
        status = Status.objects.get(name="Active").id
        UserObjectGroup.objects.create(name="deleteableobj1")
        UserObjectGroup.objects.create(name="deleteableobj2")
        UserObjectGroup.objects.create(name="deleteableobj3")
        cls.form_data = {"name": "test1", "user_objects": [user.id], "status": status}
        cls.csv_data = (
            "name,user_objects,status",
            f'csvobj1,"{user.id}",Active',
            f'csvobj2,"{user.id}",Active',
            f'csvobj3,"{user.id}",Active',
        )


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
        fixtures.create_zone()
        cls.csv_data = (
            "name,status",
            "csvobj1,Active",
            "csvobj2,Active",
            "csvobj3,Active",
        )


class PolicyRuleUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the PolicyRule viewsets."""

    model = PolicyRule
    bulk_edit_data = {"description": "bulk test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        fixtures.create_policy_rule()
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
        cls.csv_data = (
            "name,action,index,status",
            "csvobj1,deny,1,Active",
            "csvobj2,deny,2,Active",
            "csvobj3,deny,3,Active",
        )


class PolicyUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the Policy viewsets."""

    model = Policy
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        fixtures.create_policy()
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
        cls.csv_data = (
            "name,policy_rules,status",
            f'csvobj1,"{pol_rule.id}",Active',
            f'csvobj2,"{pol_rule.id}",Active',
            f'csvobj3,"{pol_rule.id}",Active',
        )


class NATPolicyRuleUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the Policy viewsets."""

    model = NATPolicyRule
    bulk_edit_data = {"log": False}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        fixtures.create_natpolicy_rule()
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
        cls.csv_data = (
            "name,log,status",
            "csvrule1,True,Active",
            "csvrule2,True,Active",
            "csvrule3,True,Active",
        )


class NATPolicyUIViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    """Test the Policy viewsets."""

    model = NATPolicy
    bulk_edit_data = {"description": "test update description"}

    @classmethod
    def setUpTestData(cls):
        """Create test data for API calls."""
        fixtures.create_natpolicy()
        status = Status.objects.get(name="Active").id
        nat_pol_rule = NATPolicyRule.objects.first()
        NATPolicy.objects.create(name="deleteableobj1")
        NATPolicy.objects.create(name="deleteableobj2")
        NATPolicy.objects.create(name="deleteableobj3")
        cls.form_data = {"status": status, "name": "test 1", "nat_policy_rules": [nat_pol_rule.id]}
        cls.csv_data = (
            "name,nat_policy_rules,status",
            f'csvrule1,"{nat_pol_rule.id}",Active',
            f'csvrule2,"{nat_pol_rule.id}",Active',
            f'csvrule3,"{nat_pol_rule.id}",Active',
        )


class CapircaPolicyUIViewTest(ViewTestCases.GetObjectViewTestCase, ViewTestCases.ListObjectsViewTestCase):
    """Test the Policy viewsets."""

    model = CapircaPolicy
    allowed_number_of_tree_queries_per_view_type = {"retrieve": 1}

    @classmethod
    def setUpTestData(cls):
        """Create test data."""
        fixtures.create_capirca_env()
        for device in Device.objects.all():
            CapircaPolicy.objects.create(device=device)


class FirewallConfigUIViewTest(ViewTestCases.GetObjectViewTestCase, ViewTestCases.ListObjectsViewTestCase):
    """Test the Policy viewsets."""

    model = FirewallConfig
    allowed_number_of_tree_queries_per_view_type = {"retrieve": 1}

    @classmethod
    def setUpTestData(cls):
        """Create test data."""
        fixtures.create_firewall_config_env()
        for device in Device.objects.all():
            FirewallConfig.objects.create(device=device)
