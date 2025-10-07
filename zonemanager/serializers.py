from rest_framework import serializers
from django.contrib.auth.models import User, Group

from master.serializer import StateSerializer, DistrictSerializer, OfficeSerializer
from .models import ZoneManager,ZMDailyTarget

from rest_framework import serializers

from asm.models import ASM
from zonemanager.models import ZMDailyTarget

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




class ZMDailyTargetSerializer(serializers.ModelSerializer):
    # Make all fields required (cannot be empty)
    zone_manager = serializers.PrimaryKeyRelatedField(queryset=ZoneManager.objects.all(), allow_null=True)
    asm = serializers.PrimaryKeyRelatedField(queryset=ASM.objects.all(), allow_null=True)
    date = serializers.DateField(required=True)

    application_target = serializers.FloatField(required=True)
    pop_target = serializers.FloatField(required=True)
    esign_target = serializers.FloatField(required=True)
    new_taluk_target = serializers.FloatField(required=True)
    new_live_partners_target = serializers.FloatField(required=True)
    activations_target = serializers.FloatField(required=True)
    calls_target = serializers.FloatField(required=True)
    sd_collection_target = serializers.FloatField(required=True)

    class Meta:
        model = ZMDailyTarget
        fields = "__all__"












