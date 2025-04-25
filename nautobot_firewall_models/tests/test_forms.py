"""Test iprange forms."""

from django.test import TestCase

from nautobot_firewall_models import forms


class IPRangeTest(TestCase):
    """Test IPRange forms."""

    def test_specifying_all_fields_success(self):
        form = forms.IPRangeForm(
            data={
                "name": "Development",
                "description": "Development Testing",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_specifying_only_required_success(self):
        form = forms.IPRangeForm(
            data={
                "name": "Development",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_validate_name_iprange_is_required(self):
        form = forms.IPRangeForm(data={"description": "Development Testing"})
        self.assertFalse(form.is_valid())
        self.assertIn("This field is required.", form.errors["name"])
