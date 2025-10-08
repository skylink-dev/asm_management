from rest_framework import serializers
from .models import ASMTask
from master.models import TaskCategory
from asm.models import ASM

class ASMTaskSerializer(serializers.ModelSerializer):
    # Read-only fields for response
    zone_full_name = serializers.SerializerMethodField()
    asm_full_name = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    # Writeable fields for POST/PUT requests
    asm_id = serializers.PrimaryKeyRelatedField(
        queryset=ASM.objects.all(), source='asm', write_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=TaskCategory.objects.all(), source='category', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = ASMTask
        fields = [
            'id',
            'zone_manager',
            'zone_full_name',
            'asm_id',         # write-only input
            'asm_full_name',  # read-only output
            'category_id',    # write-only input
            'category_name',  # read-only output
            'title',
            'details',
            'start_date',
            'end_date',
            'status',
            'created_at',
            'updated_at'
        ]

    # Read-only methods for response
    def get_zone_full_name(self, obj):
        if obj.zone_manager and obj.zone_manager.user:
            user = obj.zone_manager.user
            return f"{user.first_name} {user.last_name}"
        return None

    def get_asm_full_name(self, obj):
        if obj.asm and obj.asm.user:
            user = obj.asm.user
            return f"{user.first_name} {user.last_name}"
        return None

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
