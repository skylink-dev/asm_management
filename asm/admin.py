from django.contrib import admin
from django.utils.html import format_html
from .models import ASM
from .forms import ASMForm
from .models import ASMDailyTarget


@admin.register(ASM)
class ASMAdmin(admin.ModelAdmin):
    form = ASMForm
    list_display = (
        "full_name",
        "zone_manager_name",
        "group",
        "get_states",
        "get_districts",
        "get_offices",
        "action_links",  # Edit/Delete icons
    )
    search_fields = (
        "user__first_name",
        "user__last_name",
        "zone_manager__user__first_name",
        "zone_manager__user__last_name",
        "states__name",
        "districts__name",
        "offices__name",
    )
    list_filter = (
        "zone_manager",
      
        "states",
        "districts",
        "offices",
    )
    filter_horizontal = ( "districts", "offices")  # optional for easy selection

    # Display ASM full name
    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    full_name.short_description = "ASM Name"
    full_name.admin_order_field = "user__first_name"

    # Display Zone Manager full name
    def zone_manager_name(self, obj):
        if obj.zone_manager and obj.zone_manager.user:
            return f"{obj.zone_manager.user.first_name} {obj.zone_manager.user.last_name}"
        return "-"
    zone_manager_name.short_description = "Zone Manager"
    zone_manager_name.admin_order_field = "zone_manager__user__first_name"

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

    # 🔹 Custom edit/delete icons
    def action_links(self, obj):
        return format_html(
            '<a href="{}" style="margin-right:5px;"><img src="/static/admin/img/icon-changelink.svg" alt="Edit" /></a>'
            '<a href="{}"><img src="/static/admin/img/icon-deletelink.svg" alt="Delete" /></a>',
            f"/admin/asm/asm/{obj.pk}/change/",
            f"/admin/asm/asm/{obj.pk}/delete/"
        )
    action_links.short_description = "Actions"


@admin.register(ASMDailyTarget)
class ASMDailyTargetAdmin(admin.ModelAdmin):
    list_display = ["asm", "date", "targets_achievements_table"]
    readonly_fields = ["zm_targets_display"]

    # Add filters here
    list_filter = ["asm", "zm_daily_target", "date"]
    fieldsets = (
        ("General Info", {
            "fields": ("asm", "zm_daily_target", "zm_targets_display", "date")
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
            "description": "Enter ASM target and achievement values for each category"
        }),
    )

    readonly_fields = ["zm_targets_display"]

    def zm_targets_display(self, obj):
        """Show ZM target values as read-only reference"""
        zm = obj.zm_daily_target
        if zm:
            return format_html(
                """
                <table style="border-collapse: collapse; width: 100%;">
                    <tr><th>Category</th><th>ZM Target</th></tr>
                    <tr><td>Application</td><td>{app}</td></tr>
                    <tr><td>POP</td><td>{pop}</td></tr>
                    <tr><td>E-Sign</td><td>{esign}</td></tr>
                    <tr><td>New Taluk</td><td>{new_taluk}</td></tr>
                    <tr><td>New Live Partners</td><td>{new_live}</td></tr>
                    <tr><td>Activations</td><td>{activations}</td></tr>
                    <tr><td>Calls</td><td>{calls}</td></tr>
                    <tr><td>SD Collection</td><td>{sd}</td></tr>
                </table>
                """,
                app=zm.application_target,
                pop=zm.pop_target,
                esign=zm.esign_target,
                new_taluk=zm.new_taluk_target,
                new_live=zm.new_live_partners_target,
                activations=zm.activations_target,
                calls=zm.calls_target,
                sd=zm.sd_collection_target
            )
        return "No ZM Target"

    zm_targets_display.short_description = "ZM Daily Target"

 

    def targets_achievements_table(self, obj):
        zm = obj.zm_daily_target  # ZM target

        return format_html(
            """
            <table style="border-collapse: collapse; width: 100%;">
                <thead>
                    <tr style="background-color:#f0f0f0;">
                        <th style="padding:4px 8px;">Category</th>
                        <th style="padding:4px 8px;">ZM Target</th>
                        <th style="padding:4px 8px;">ASM Target</th>
                        <th style="padding:4px 8px;">ASM Achievement</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>Application</td><td>{zm_app}</td><td>{asm_app_t}</td><td>{asm_app_a}</td></tr>
                    <tr><td>POP</td><td>{zm_pop}</td><td>{asm_pop_t}</td><td>{asm_pop_a}</td></tr>
                    <tr><td>E-Sign</td><td>{zm_esign}</td><td>{asm_esign_t}</td><td>{asm_esign_a}</td></tr>
                    <tr><td>New Taluk</td><td>{zm_new_taluk}</td><td>{asm_new_taluk_t}</td><td>{asm_new_taluk_a}</td></tr>
                    <tr><td>New Live Partners</td><td>{zm_new_live}</td><td>{asm_new_live_t}</td><td>{asm_new_live_a}</td></tr>
                    <tr><td>Activations</td><td>{zm_activations}</td><td>{asm_activations_t}</td><td>{asm_activations_a}</td></tr>
                    <tr><td>Calls</td><td>{zm_calls}</td><td>{asm_calls_t}</td><td>{asm_calls_a}</td></tr>
                    <tr><td>SD Collection</td><td>{zm_sd}</td><td>{asm_sd_t}</td><td>{asm_sd_a}</td></tr>
                </tbody>
            </table>
            """,
            zm_app=zm.application_target if zm else "-",
            zm_pop=zm.pop_target if zm else "-",
            zm_esign=zm.esign_target if zm else "-",
            zm_new_taluk=zm.new_taluk_target if zm else "-",
            zm_new_live=zm.new_live_partners_target if zm else "-",
            zm_activations=zm.activations_target if zm else "-",
            zm_calls=zm.calls_target if zm else "-",
            zm_sd=zm.sd_collection_target if zm else "-",

            asm_app_t=obj.application_target,
            asm_app_a=obj.application_achieve,
            asm_pop_t=obj.pop_target,
            asm_pop_a=obj.pop_achieve,
            asm_esign_t=obj.esign_target,
            asm_esign_a=obj.esign_achieve,
            asm_new_taluk_t=obj.new_taluk_target,
            asm_new_taluk_a=obj.new_taluk_achieve,
            asm_new_live_t=obj.new_live_partners_target,
            asm_new_live_a=obj.new_live_partners_achieve,
            asm_activations_t=obj.activations_target,
            asm_activations_a=obj.activations_achieve,
            asm_calls_t=obj.calls_target,
            asm_calls_a=obj.calls_achieve,
            asm_sd_t=obj.sd_collection_target,
            asm_sd_a=obj.sd_collection_achieve,
        )

    targets_achievements_table.short_description = "ZM vs ASM Targets & Achievements"
