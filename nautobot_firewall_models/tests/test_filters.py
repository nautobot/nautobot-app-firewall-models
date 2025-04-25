"""Test IPRange Filter."""

from nautobot.apps.testing import FilterTestCases

from nautobot_firewall_models import filters, models
from nautobot_firewall_models.tests import fixtures


class IPRangeFilterTestCase(FilterTestCases.FilterTestCase):
    """IPRange Filter Test Case."""

    queryset = models.IPRange.objects.all()
    filterset = filters.IPRangeFilterSet
    generic_filter_tests = (
        ("id",),
        ("created",),
        ("last_updated",),
        ("name",),
    )

    @classmethod
    def setUpTestData(cls):
        """Setup test data for IPRange Model."""
        fixtures.create_iprange()

    def test_q_search_name(self):
        """Test using Q search with name of IPRange."""
        params = {"q": "Test One"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_q_invalid(self):
        """Test using invalid Q search for IPRange."""
        params = {"q": "test-five"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 0)
