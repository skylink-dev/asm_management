from django.contrib import admin
from .models import Role, ASM, ASMTalukMapping, ASMStateMapping, ASMZoneMapping, ASMDistrictMapping


class ASMTalukMappingInline(admin.TabularInline):
    model = ASMTalukMapping
    extra = 1   # show one empty row by default
    autocomplete_fields = ["region_id"]


class ASMStateMappingInline(admin.TabularInline):
    model = ASMStateMapping
    extra = 1
    autocomplete_fields = ["state_id"]


class ASMZoneMappingInline(admin.TabularInline):
    model = ASMZoneMapping
    extra = 1
    autocomplete_fields = ["zone_id"]


class ASMDistrictMappingInline(admin.TabularInline):
    model = ASMDistrictMapping
    extra = 1
    autocomplete_fields = ["district_id"]

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "isActive")
    search_fields = ("name",)


@admin.register(ASM)
class ASMAdmin(admin.ModelAdmin):
    list_display = (
        "id", "code", "user", "get_user_email", "role", "status",
        "last_login", "last_password_change", "otp_allowed", "otp_used", "created_at"
    )
    list_filter = ("status", "otp_allowed", "otp_used", "role")
    search_fields = ("code", "user__username", "user__email")
    ordering = ("-created_at",)

    # custom column to show User email
    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = "User Email"

    inlines = [
        ASMTalukMappingInline,
        ASMStateMappingInline,
        ASMZoneMappingInline,
        ASMDistrictMappingInline,
    ]


@admin.register(ASMTalukMapping)
class ASMTalukMappingAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "asm_id", "region_id")
    search_fields = ("code", "asm_id__code", "region_id__name")
    list_filter = ("region_id",)


@admin.register(ASMStateMapping)
class ASMStateMappingAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "asm_id", "state_id")
    search_fields = ("code", "asm_id__code", "state_id__name")
    list_filter = ("state_id",)


@admin.register(ASMZoneMapping)
class ASMZoneMappingAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "asm_id", "zone_id")
    search_fields = ("code", "asm_id__code", "zone_id__name")
    list_filter = ("zone_id",)


@admin.register(ASMDistrictMapping)
class ASMDistrictMappingAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "asm_id", "district_id")
    search_fields = ("code", "asm_id__code", "district_id__name")
    list_filter = ("district_id",)




