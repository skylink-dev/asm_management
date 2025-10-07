# zonemanager/views.py
from dal import autocomplete
from django.contrib.auth.models import User
from master.models import District, Office

class DistrictAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = District.objects.all()
        states = self.forwarded.get('states', None)
        if states:
            qs = qs.filter(state__id__in=states)
        return qs

class OfficeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Office.objects.all()
        districts = self.forwarded.get('districts', None)
        if districts:
            qs = qs.filter(district__id__in=districts)
        return qs



