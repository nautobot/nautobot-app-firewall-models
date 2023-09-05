"""Unit tests for nautobot_firewall_models."""
# pylint: disable=invalid-name

from django.test import TestCase

from nautobot.dcim.models import Device
from nautobot_firewall_models import filters, models

from .fixtures import create_capirca_env


class CapircaPolicyModelTestCase(TestCase):
    """Test filtering operations for CapircaPolicy Model."""

    queryset = models.CapircaPolicy.objects.all()
    filterset = filters.CapircaPolicyFilterSet

    def setUp(self):
        """Set up base objects."""
        create_capirca_env()
        self.dev01 = Device.objects.get(name="DFW-WAN00")
        dev02 = Device.objects.get(name="HOU-WAN00")
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
        params = {"device_id": [self.dev01.id]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)
