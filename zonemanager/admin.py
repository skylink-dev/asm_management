from django.contrib import admin
from django.utils.html import format_html
from .models import ZoneManager, ZMDailyTarget
from .forms import ZoneManagerForm
from dal import autocomplete

@admin.register(ZoneManager)
class ZoneManagerAdmin(admin.ModelAdmin):
    form = ZoneManagerForm

    list_display = (
        "full_name",
        "group",
        "get_states",
        "get_districts",
        "get_offices",
        "action_links",
    )

    search_fields = (
        "user__first_name",
        "user__last_name",
        "states__name",
        "districts__name",
        "offices__name",
    )

    list_filter = (
        "states",
        "districts",
        "offices",
    )

    # Remove filter_horizontal for chained fields
    # filter_horizontal = ("districts", "offices")

    # Display full name
    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}" if obj.user else "-"
    full_name.short_description = "Zone Manager Name"
    full_name.admin_order_field = "user__first_name"

    # Display States
    def get_states(self, obj):
        return ", ".join([s.name for s in obj.states.all()])
    get_states.short_description = "States"

    # Display Districts
    def get_districts(self, obj):
        return ", ".join([d.name for d in obj.districts.all()])
    get_districts.short_description = "Districts"

    # Display Offices
    def get_offices(self, obj):
        return ", ".join([o.name for o in obj.offices.all()])
    get_offices.short_description = "Offices"

    # Custom edit/delete icons
    def action_links(self, obj):
        return format_html(
            '<a href="{}" style="margin-right:5px;"><img src="/static/admin/img/icon-changelink.svg" alt="Edit" /></a>'
            '<a href="{}"><img src="/static/admin/img/icon-deletelink.svg" alt="Delete" /></a>',
            f"/admin/zonemanager/zonemanager/{obj.pk}/change/",
            f"/admin/zonemanager/zonemanager/{obj.pk}/delete/"
        )
    action_links.short_description = "Actions"

    # Include JS for chained fields
    class Media:
        js = [
            "admin/js/jquery.init.js",       # Required by Django admin
            "js/admin/chained_fields.js",    # Your custom JS
        ]

@admin.register(ZMDailyTarget)
class ZMDailyTargetAdmin(admin.ModelAdmin):
    list_display = ("date", "zone_manager_name", "asm_name", "targets_achievements_table")
    list_filter = ("zone_manager", "asm", "date")
    search_fields = (
        "zone_manager__user__first_name",
        "zone_manager__user__last_name",
        "asm__user__first_name",
        "asm__user__last_name",
    )

    # Group fields in the add/change form
    fieldsets = (
        ("General Info", {
            "fields": ("zone_manager", "asm", "date")
        }),
        ("Targets & Achievements", {
            "fields": (
                ("application_target", "application_achieve"),
                ("pop_target", "pop_achieve"),
                ("esign_target", "esign_achieve"),
                ("new_taluk_target", "new_taluk_achieve"),
                ("new_live_partners_target", "new_live_partners_achieve"),
                ("activations_target", "activations_achieve"),
                ("calls_target", "calls_achieve"),
                ("sd_collection_target", "sd_collection_achieve"),
            ),
            "description": "Enter target and achievement values for each category"
        }),
    )

    # Display Zone Manager name
    def zone_manager_name(self, obj):
        if obj.zone_manager and obj.zone_manager.user:
            return f"{obj.zone_manager.user.first_name} {obj.zone_manager.user.last_name}"
        return "-"
    zone_manager_name.short_description = "Zone Manager"

    # Display ASM name
    def asm_name(self, obj):
        if obj.asm and obj.asm.user:
            return f"{obj.asm.user.first_name} {obj.asm.user.last_name}"
        return "-"
    asm_name.short_description = "ASM"

    # Table for list_display
    def targets_achievements_table(self, obj):
        return format_html(
            """
            <table style="border-collapse: collapse; width: 100%;">
                <thead>
                    <tr style="background-color:#f0f0f0;">
                        <th style="padding:4px 8px;">Category</th>
                        <th style="padding:4px 8px;">Target</th>
                        <th style="padding:4px 8px;">Achievement</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>Application</td><td>{app_t}</td><td>{app_a}</td></tr>
                    <tr><td>POP</td><td>{pop_t}</td><td>{pop_a}</td></tr>
                    <tr><td>E-Sign</td><td>{esign_t}</td><td>{esign_a}</td></tr>
                    <tr><td>New Taluk</td><td>{new_taluk_t}</td><td>{new_taluk_a}</td></tr>
                    <tr><td>New Live Partners</td><td>{new_live_t}</td><td>{new_live_a}</td></tr>
                    <tr><td>Activations</td><td>{activations_t}</td><td>{activations_a}</td></tr>
                    <tr><td>Calls</td><td>{calls_t}</td><td>{calls_a}</td></tr>
                    <tr><td>SD Collection</td><td>{sd_t}</td><td>{sd_a}</td></tr>
                </tbody>
            </table>
            """,
            app_t=obj.application_target,
            app_a=obj.application_achieve,
            pop_t=obj.pop_target,
            pop_a=obj.pop_achieve,
            esign_t=obj.esign_target,
            esign_a=obj.esign_achieve,
            new_taluk_t=obj.new_taluk_target,
            new_taluk_a=obj.new_taluk_achieve,
            new_live_t=obj.new_live_partners_target,
            new_live_a=obj.new_live_partners_achieve,
            activations_t=obj.activations_target,
            activations_a=obj.activations_achieve,
            calls_t=obj.calls_target,
            calls_a=obj.calls_achieve,
            sd_t=obj.sd_collection_target,
            sd_a=obj.sd_collection_achieve,
        )
    targets_achievements_table.short_description = "Targets & Achievements"