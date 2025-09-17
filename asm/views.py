from dal import autocomplete
from zonemanager.models import ZoneManager
from master.models import District, Office

class ZoneManagerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ZoneManager.objects.all()
        if self.q:
            qs = qs.filter(user__username__icontains=self.q)
        return qs

# Optional: You can reuse your existing district & office autocomplete views
