from dal import autocomplete
from django.contrib.auth.models import User
from zonemanager.models import ZoneManager
from asm.models import ASM
from master.models import District, Office

# 🔹 Zone Manager Autocomplete
class ZoneManagerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ZoneManager.objects.all()
        if self.q:
            qs = qs.filter(user__first_name__icontains=self.q) | qs.filter(user__last_name__icontains=self.q)
        return qs

# 🔹 ASM Autocomplete (filtered by selected Zone Manager)
class ASMAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ASM.objects.all()
        zone_manager_id = self.forwarded.get('zone_manager', None)
        if zone_manager_id:
            qs = qs.filter(zone_manager_id=zone_manager_id)
        if self.q:
            qs = qs.filter(user__first_name__icontains=self.q) | qs.filter(user__last_name__icontains=self.q)
        return qs

# 🔹 District Autocomplete (filtered by selected States)
class DistrictAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = District.objects.all()
        states_ids = self.forwarded.get('states', None)
        if states_ids:
            qs = qs.filter(state_id__in=states_ids)
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

# 🔹 Office Autocomplete (filtered by selected Districts)
class OfficeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Office.objects.all()
        districts_ids = self.forwarded.get('districts', None)
        if districts_ids:
            qs = qs.filter(district_id__in=districts_ids)
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs



