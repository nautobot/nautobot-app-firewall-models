"""Test IPRange."""

from nautobot.apps.testing import ModelTestCases

from nautobot_firewall_models import models
from nautobot_firewall_models.tests import fixtures


class TestIPRange(ModelTestCases.BaseModelTestCase):
    """Test IPRange."""

    model = models.IPRange

    @classmethod
    def setUpTestData(cls):
        """Create test data for IPRange Model."""
        super().setUpTestData()
        # Create 3 objects for the model test cases.
        fixtures.create_iprange()

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
