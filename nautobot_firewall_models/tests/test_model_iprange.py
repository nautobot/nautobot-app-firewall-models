"""Test IPRange."""

from django.test import TestCase

from nautobot_firewall_models import models


class TestIPRange(TestCase):
    """Test IPRange."""

    def test_create_iprange_only_required(self):
        """Create with only required fields, and validate null description and __str__."""
        iprange = models.IPRange.objects.create(name="Development")
        self.assertEqual(iprange.name, "Development")
        self.assertEqual(iprange.description, "")
        self.assertEqual(str(iprange), "Development")

    def test_create_iprange_all_fields_success(self):
        """Create IPRange with all fields."""
        iprange = models.IPRange.objects.create(name="Development", description="Development Test")
        self.assertEqual(iprange.name, "Development")
        self.assertEqual(iprange.description, "Development Test")
