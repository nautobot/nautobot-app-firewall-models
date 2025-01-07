"""Create fixtures for tests."""

from nautobot_firewall_models.models import IPRange


def create_iprange():
    """Fixture to create necessary number of IPRange for tests."""
    IPRange.objects.create(name="Test One")
    IPRange.objects.create(name="Test Two")
    IPRange.objects.create(name="Test Three")
