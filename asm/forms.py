from django import forms
#from dal import autocomplete
from .models import ASM


class ASMForm(forms.ModelForm):

    class Meta:
        model = ASM
        fields = ['user', 'zone_manager', 'group', 'states', 'districts', 'offices']

        # widgets = {
        #     #'zone_manager': autocomplete.ModelSelect2(url='zonemanager-autocomplete'),
        #     'districts': autocomplete.ModelSelect2Multiple(
        #         url='district-autocomplete',
        #         forward=['states']
        #     ),
        #     'offices': autocomplete.ModelSelect2Multiple(
        #         url='office-autocomplete',
        #         forward=['districts']
        #     ),
        # }
