from django.contrib import admin
from .models import Zone, State, District, Taluk









@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'description')
    search_fields = ('name', 'code')
    list_per_page = 20


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'zone', 'description')
    search_fields = ('name', 'code', 'zone__name')
    list_filter = ('zone',)
    list_per_page = 20


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'state', 'description')
    search_fields = ('name', 'code', 'state__name')
    list_filter = ('state',)
    list_per_page = 20


@admin.register(Taluk)
class TalukAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'district', 'description')
    search_fields = ('name', 'code', 'district__name')
    list_filter = ('district',)
    list_per_page = 20
