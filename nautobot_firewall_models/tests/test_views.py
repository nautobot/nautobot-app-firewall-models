"""Unit tests for views."""

from nautobot.apps.testing import ViewTestCases

from nautobot_firewall_models import models
from nautobot_firewall_models.tests import fixtures


class IPRangeViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=too-many-ancestors
    """Test the IPRange views."""

    model = models.IPRange
    bulk_edit_data = {"description": "Bulk edit views"}
    form_data = {
        "name": "Test 1",
        "description": "Initial model",
    }

    update_data = {
        "name": "Test 2",
        "description": "Updated model",
    }

    @classmethod
    def setUpTestData(cls):
        fixtures.create_iprange()
