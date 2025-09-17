from django.urls import path
from .views import ZoneManagerAutocomplete

urlpatterns = [
    path('zonemanager-autocomplete/', ZoneManagerAutocomplete.as_view(), name='zonemanager-autocomplete'),
]
