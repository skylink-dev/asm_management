# zonemanager/urls.py
from django.urls import path

from asm.views import ZoneManagerAutocomplete
from . import views

urlpatterns = [
    path('district-autocomplete/', views.DistrictAutocomplete.as_view(), name='district-autocomplete'),
    path('office-autocomplete/', views.OfficeAutocomplete.as_view(), name='office-autocomplete'),
    path('zonemanager-autocomplete/', ZoneManagerAutocomplete.as_view(), name='zonemanager-autocomplete'),
]
