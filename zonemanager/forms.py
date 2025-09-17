# zonemanager/forms.py
from django import forms
from dal import autocomplete
from .models import ZoneManager
from master.models import State, District, Office

class ZoneManagerForm(forms.ModelForm):
    districts = forms.ModelMultipleChoiceField(
        queryset=District.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            url='district-autocomplete',
            forward=['states']
        ),
        required=False
    )
    offices = forms.ModelMultipleChoiceField(
        queryset=Office.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(
            url='office-autocomplete',
            forward=['districts']
        ),
        required=False
    )

    class Meta:
        model = ZoneManager
        fields = '__all__'
