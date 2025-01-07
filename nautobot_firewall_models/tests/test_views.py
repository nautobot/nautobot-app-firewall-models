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
    csv_data = (
        "name",
        "Test csv1",
        "Test csv2",
        "Test csv3",
    )

    @classmethod
    def setUpTestData(cls):
        fixtures.create_iprange()
