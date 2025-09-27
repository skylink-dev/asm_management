from rest_framework import serializers
from django.contrib.auth.models import User, Group
from asm.serializers import GroupSerializer
from master.serializer import StateSerializer, DistrictSerializer, OfficeSerializer
from .models import ZoneManager

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