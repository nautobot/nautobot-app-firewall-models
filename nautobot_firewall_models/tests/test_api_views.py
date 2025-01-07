"""Unit tests for nautobot_firewall_models."""

from nautobot.apps.testing import APIViewTestCases

from nautobot_firewall_models import models
from nautobot_firewall_models.tests import fixtures


class IPRangeAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=too-many-ancestors
    """Test the API viewsets for IPRange."""

    model = models.IPRange
    create_data = [
        {
            "name": "Test Model 1",
            "description": "test description",
        },
        {
            "name": "Test Model 2",
        },
    ]
    bulk_update_data = {"description": "Test Bulk Update"}

    @classmethod
    def setUpTestData(cls):
        fixtures.create_iprange()
