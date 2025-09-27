from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import PincodeData
from .resources import PincodeDataResource

from .models import State, District, Office

@admin.register(PincodeData)
class PincodeDataAdmin(ImportExportModelAdmin):
    resource_class = PincodeDataResource
    list_display = ("officename", "pincode", "district", "statename", "officetype", "delivery")
    search_fields = ("officename", "pincode", "district", "statename")
    list_filter = ("statename", "district", "officetype", "delivery")


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    # No filters needed for State as it is top-level


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("name", "state")
    search_fields = ("name", "state__name")
    list_filter = ("state",)  # Filter districts by State


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ("name", "district", "officetype", "pincode")
    search_fields = ("name", "district__name", "pincode")
    list_filter = ("district__state", "district", "officetype") 