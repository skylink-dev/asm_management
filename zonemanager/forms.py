# zonemanager/forms.py
from django import forms
from dal import autocomplete
from .models import ZoneManager
from master.models import State, District, Office


class ZoneManagerForm(forms.ModelForm):
    class Meta:
        model = ZoneManager
        fields = ['user', 'group', 'states', 'districts', 'offices']

        widgets = {
            'districts': autocomplete.ModelSelect2Multiple(
                url='district-autocomplete',
                forward=['states']
            ),
            'offices': autocomplete.ModelSelect2Multiple(
                url='office-autocomplete',
                forward=['districts']
            ),
        }
