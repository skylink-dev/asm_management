# zonemanager/admin.py
from django.contrib import admin
from .models import ZoneManager
from .forms import ZoneManagerForm

@admin.register(ZoneManager)
class ZoneManagerAdmin(admin.ModelAdmin):
    form = ZoneManagerForm
    list_display = ("user", "group")
