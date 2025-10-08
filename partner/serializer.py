from rest_framework import serializers
from .models import SDCollection, Partner
from asm.models import ASM
from zonemanager.models import ZoneManager

# 1️⃣ Partner Serializer
class PartnerBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ['id', 'name', 'email']

# 2️⃣ ASM Serializer
class ASMBasicSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "username": obj.user.username,
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
        }

    class Meta:
        model = ASM
        fields = ['id', 'user']

# 3️⃣ Zone Manager Serializer
class ZoneManagerBasicSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "username": obj.user.username,
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
        }

    class Meta:
        model = ZoneManager
        fields = ['id', 'user']

# 4️⃣ SDCollection Serializer with nested objects
class SDCollectionSerializer(serializers.ModelSerializer):
    partner = PartnerBasicSerializer(read_only=True)
    asm = ASMBasicSerializer(read_only=True)
    zone_manager = ZoneManagerBasicSerializer(read_only=True)

    class Meta:
        model = SDCollection
        fields = [
            'id',
            'partner',
            'asm',
            'zone_manager',
            'date',
            'amount',
            'note',
            'status',
        ]
