"""Unit tests for nautobot_firewall_models."""
# pylint: disable=invalid-name

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from nautobot.dcim.models import Device

from nautobot_firewall_models import filters, models

from .fixtures import create_aerleon_env


class AerleonPolicyModelTestCase(TestCase):
    """Test filtering operations for AerleonPolicy Model."""

    queryset = models.AerleonPolicy.objects.all()
    filterset = filters.AerleonPolicyFilterSet

    def setUp(self):
        """Set up base objects."""
        create_aerleon_env()
        ct = ContentType.objects.get_for_model(Device)

        self.dev01 = Device.objects.get(name="DFW02-WAN00")
        dev02 = Device.objects.get(name="HOU02-WAN00")
        models.AerleonPolicy.objects.create(content_type=ct, object_id=self.dev01.id)
        models.AerleonPolicy.objects.create(content_type=ct, object_id=dev02.id)

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
        params = {"device_id": [self.dev01.id]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
