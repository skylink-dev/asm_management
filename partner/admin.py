from django.contrib import admin
from django.utils.html import format_html
from .models import Partner
from .forms import PartnerForm

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    form = PartnerForm
    list_display = (
        "name",
        "email",
        "zone_manager_name",
        "asm_name",
        "get_states",
        "get_districts",
        "get_offices",
        "action_links",
    )
    search_fields = (
        "name",
        "email",
        "zone_manager__user__first_name",
        "zone_manager__user__last_name",
        "asm__user__first_name",
        "asm__user__last_name",
        "states__name",
        "districts__name",
        "offices__name",
    )
    list_filter = (
        "zone_manager",
        "asm",
        "states",
        "districts",
        "offices",
    )
    filter_horizontal = ( "districts", "offices")

    def zone_manager_name(self, obj):
        if obj.zone_manager:
            return f"{obj.zone_manager.user.first_name} {obj.zone_manager.user.last_name}"
        return "-"
    zone_manager_name.short_description = "Zone Manager"

    def asm_name(self, obj):
        if obj.asm:
            return f"{obj.asm.user.first_name} {obj.asm.user.last_name}"
        return "-"
    asm_name.short_description = "ASM"

    def get_states(self, obj):
        return ", ".join([s.name for s in obj.states.all()])
    get_states.short_description = "States"

    def get_districts(self, obj):
        return ", ".join([d.name for d in obj.districts.all()])
    get_districts.short_description = "Districts"

    def get_offices(self, obj):
        return ", ".join([o.name for o in obj.offices.all()])
    get_offices.short_description = "Offices"

    def action_links(self, obj):
        return format_html(
            '<a href="{}" style="margin-right:5px;"><img src="/static/admin/img/icon-changelink.svg" alt="Edit" /></a>'
            '<a href="{}"><img src="/static/admin/img/icon-deletelink.svg" alt="Delete" /></a>',
            f"/admin/partner/partner/{obj.pk}/change/",
            f"/admin/partner/partner/{obj.pk}/delete/"
        )
    action_links.short_description = "Actions"
