from django import forms
from dal import autocomplete
from .models import Partner
from zonemanager.models import ZoneManager
from asm.models import ASM

class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ["name", "email", "zone_manager", "asm", "states", "districts", "offices"]

        widgets = {
            "zone_manager": autocomplete.ModelSelect2(url="zone-manager-autocomplete"),
            "asm": autocomplete.ModelSelect2(url="asm-autocomplete", forward=["zone_manager"]),
            "districts": autocomplete.ModelSelect2Multiple(
                url="district-autocomplete",
                forward=["states"]
            ),
            "offices": autocomplete.ModelSelect2Multiple(
                url="office-autocomplete",
                forward=["districts"]
            ),
        }
