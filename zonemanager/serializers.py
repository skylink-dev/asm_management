from rest_framework import serializers
from django.contrib.auth.models import User, Group

from master.serializer import StateSerializer, DistrictSerializer, OfficeSerializer
from .models import ZMDailyTarget
from asm.models import ASM
from zonemanager.models import ZoneManager


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]


class UserBasicSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name']

    def get_full_name(self, obj):
        return obj.get_full_name()


class ZoneManagerSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer(read_only=True)
    group = GroupSerializer(read_only=True)
    states = StateSerializer(many=True, read_only=True)
    districts = DistrictSerializer(many=True, read_only=True)
    offices = OfficeSerializer(many=True, read_only=True)

    class Meta:
        model = ZoneManager
        fields = [
            'id',
            'user',
            'group',
            'states',
            'districts',
            'offices',
        ]




# class ZMDailyTargetSerializer(serializers.ModelSerializer):
#     # Make all fields required (cannot be empty)
#     zone_manager = serializers.PrimaryKeyRelatedField(queryset=ZoneManager.objects.all(), allow_null=True)
#     asm = serializers.PrimaryKeyRelatedField(queryset=ASM.objects.all(), allow_null=True)
#     date = serializers.DateField(required=True)
#
#     application_target = serializers.FloatField(required=True)
#     pop_target = serializers.FloatField(required=True)
#     esign_target = serializers.FloatField(required=True)
#     new_taluk_target = serializers.FloatField(required=True)
#     new_live_partners_target = serializers.FloatField(required=True)
#     activations_target = serializers.FloatField(required=True)
#     calls_target = serializers.FloatField(required=True)
#     sd_collection_target = serializers.FloatField(required=True)
#
#     class Meta:
#         model = ZMDailyTarget
#         fields = "__all__"
#
#


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

#
class ZoneManagerSerializerOnlyName(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = ZoneManager
        fields = ['id', 'user']  # include only id and name

class ASMSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = ASM
        fields = ['id', 'user']


class ZMDailyTargetSerializer(serializers.ModelSerializer):
    zone_manager_id = serializers.PrimaryKeyRelatedField(
        queryset=ZoneManager.objects.all(), source='zone_manager', write_only=True
    )
    asm_id = serializers.PrimaryKeyRelatedField(
        queryset=ASM.objects.all(), source='asm', write_only=True
    )
    zone_manager = ZoneManagerSerializerOnlyName(read_only=True)
    asm = ASMSerializer(read_only=True)

    application_target = serializers.FloatField(required=True)
    pop_target = serializers.FloatField(required=True)
    esign_target = serializers.FloatField(required=True)
    new_taluk_target = serializers.FloatField(required=True)
    new_live_partners_target = serializers.FloatField(required=True)
    activations_target = serializers.FloatField(required=True)
    calls_target = serializers.FloatField(required=True)
    sd_collection_target = serializers.FloatField(required=True)

    # Achieve fields (default 0)
    application_achieve = serializers.FloatField(default=0.0)
    pop_achieve = serializers.FloatField(default=0.0)
    esign_achieve = serializers.FloatField(default=0.0)
    new_taluk_achieve = serializers.FloatField(default=0.0)
    new_live_partners_achieve = serializers.FloatField(default=0.0)
    activations_achieve = serializers.FloatField(default=0.0)
    calls_achieve = serializers.FloatField(default=0.0)
    sd_collection_achieve = serializers.FloatField(default=0.0)

    class Meta:
        model = ZMDailyTarget
        fields = "__all__"

