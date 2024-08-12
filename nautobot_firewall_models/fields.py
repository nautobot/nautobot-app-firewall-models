"""Creating fields for IPRange models."""

from django import forms
from nautobot.ipam.formfields import IPAddressFormField


class IPRangeFieldMixin(forms.ModelForm):
    """ModelForm mixin for IP Address based models."""

    start_address = IPAddressFormField()
    end_address = IPAddressFormField()

    def __init__(self, *args, **kwargs):
        """Overload init to account for computed field."""
        instance = kwargs.get("instance")
        initial = kwargs.get("initial", {}).copy()
        # If initial already has a `address`, we want to use that `address` as it was passed into
        # the form. If we're editing an object with a `address` field, we need to patch initial
        # to include `address` because it is a computed field.
        if instance.start_address != b"":
            initial["start_address"] = instance.start_address
        if instance.end_address != b"":
            initial["end_address"] = instance.end_address

        kwargs["initial"] = initial

        super().__init__(*args, **kwargs)

    def clean(self):
        """Overload clean to properly set attrs."""
        super().clean()

        # Need to set instance attribute for `start_address` & `end_address` to run proper validation on Model.clean()
        self.instance.start_address = self.cleaned_data.get("start_address")
        self.instance.end_address = self.cleaned_data.get("end_address")
