"""Unit tests for nautobot_firewall_models."""

# pylint: disable=invalid-name

from django.test import TestCase
from nautobot.apps.testing import FilterTestCases
from nautobot.dcim.models import Device
from nautobot.extras.models import Status
from nautobot.ipam.models import IPAddress, Namespace, Prefix

from nautobot_firewall_models import filters, models
from nautobot_firewall_models.models import UserObject

from .fixtures import create_capirca_env


class CapircaPolicyModelTestCase(TestCase):
    """Test filtering operations for CapircaPolicy Model."""

    queryset = models.CapircaPolicy.objects.all()
    filterset = filters.CapircaPolicyFilterSet

    def setUp(self):
        """Set up base objects."""
        create_capirca_env()
        self.dev01 = Device.objects.get(name="DFW02-WAN00")
        dev02 = Device.objects.get(name="HOU02-WAN00")
        models.CapircaPolicy.objects.create(device=self.dev01)
        models.CapircaPolicy.objects.create(device=dev02)

    def test_id(self):
        """Test filtering by ID (primary key)."""
        params = {"id": str(self.queryset.values_list("pk", flat=True)[0])}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_full(self):
        """Test without filtering to ensure all devices have been added."""
        self.assertEqual(self.queryset.count(), 2)

    def test_device(self):
        """Test filtering by Device."""
        params = {"device": [self.dev01.name]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
        params = {"device": [self.dev01.id]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)


class AddressObjectTestCase(FilterTestCases.FilterTestCase):
    """Test filtering operations for AddressObject Model."""

    queryset = models.AddressObject.objects.all()
    filterset = filters.AddressObjectFilterSet
    generic_filter_tests = (
        ("address_object_groups", "address_object_groups__id"),
        ("address_object_groups", "address_object_groups__name"),
    )

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        status_active = Status.objects.get(name="Active")
        global_namespace = Namespace.objects.get(name="Global")
        Prefix.objects.create(prefix="0.0.0.0/0", namespace=global_namespace, status=status_active)
        ip_addresses = (
            IPAddress.objects.create(address="10.0.0.1", status=status_active, namespace=global_namespace),
            IPAddress.objects.create(address="10.0.0.2", status=status_active, namespace=global_namespace),
            IPAddress.objects.create(address="10.0.0.3", status=status_active, namespace=global_namespace),
        )
        address_objects = (
            models.AddressObject.objects.create(
                name="test-address-object",
                status=status_active,
                ip_address=ip_addresses[0],
            ),
            models.AddressObject.objects.create(
                name="test-address-object-2",
                status=status_active,
                ip_address=ip_addresses[1],
            ),
            models.AddressObject.objects.create(
                name="test-address-object-3",
                status=status_active,
                ip_address=ip_addresses[2],
            ),
        )
        address_object_groups = (
            models.AddressObjectGroup.objects.create(name="test-address-object-group", status=status_active),
            models.AddressObjectGroup.objects.create(name="test-address-object-group-2", status=status_active),
            models.AddressObjectGroup.objects.create(name="test-address-object-group-3", status=status_active),
        )
        address_object_groups[0].address_objects.set([address_objects[0]])
        address_object_groups[1].address_objects.set([address_objects[1]])
        address_object_groups[2].address_objects.set([address_objects[2]])


class ApplicationObjectTestCase(FilterTestCases.FilterTestCase):
    """Test filtering operations for ApplicationObject Model."""

    queryset = models.ApplicationObject.objects.all()
    filterset = filters.ApplicationObjectFilterSet
    generic_filter_tests = (
        ("application_object_groups", "application_object_groups__id"),
        ("application_object_groups", "application_object_groups__name"),
    )

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        status_active = Status.objects.get(name="Active")
        application_objects = (
            models.ApplicationObject.objects.create(
                name="test-application-object",
                status=status_active,
            ),
            models.ApplicationObject.objects.create(
                name="test-application-object-2",
                status=status_active,
            ),
            models.ApplicationObject.objects.create(
                name="test-application-object-3",
                status=status_active,
            ),
        )
        application_object_groups = (
            models.ApplicationObjectGroup.objects.create(name="test-application-object-group", status=status_active),
            models.ApplicationObjectGroup.objects.create(name="test-application-object-group-2", status=status_active),
            models.ApplicationObjectGroup.objects.create(name="test-application-object-group-3", status=status_active),
        )
        application_object_groups[0].application_objects.set([application_objects[0]])
        application_object_groups[1].application_objects.set([application_objects[1]])
        application_object_groups[2].application_objects.set([application_objects[2]])


class UserObjectTestCase(FilterTestCases.FilterTestCase):
    """Test filtering operations for ApplicationObject Model."""

    queryset = models.UserObject.objects.all()
    filterset = filters.UserObjectFilterSet

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""

        status_active = Status.objects.get(name="Active")
        UserObject.objects.get_or_create(
            username="user1",
            name="Bob",
            status=status_active,
        )
        UserObject.objects.get_or_create(
            username="user2",
            name="Fred",
            status=status_active,
        )
        UserObject.objects.get_or_create(
            username="user3",
            name="Tom",
            status=status_active,
        )

    def test_q_filter_name(self):
        """Test q filter on name field"""
        params = {"q": "Bob"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_q_filter_username(self):
        """Test q filter on username field"""
        params = {"q": "user2"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
