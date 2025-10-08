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

from rest_framework import serializers
from .models import ZMDailyTarget,  ZoneManager

from zonemanager.models import ZoneManager, ZMDailyTarget  # Only models in this app
from asm.models import ASM  # Import ASM from its app

# Nested serializers (if in a separate file)
# from .nested_serializers import ASMSerializer, ZoneManagerSerializerOnlyName
class ZMDailyTargetSerializer(serializers.ModelSerializer):
    # Input fields (write-only)
    zone_manager_id = serializers.PrimaryKeyRelatedField(
        queryset=ZoneManager.objects.all(),
        source='zone_manager',
        write_only=True
    )
    asm_id = serializers.PrimaryKeyRelatedField(
        queryset=ASM.objects.all(),
        source='asm',
        write_only=True
    )

    # Output fields (read-only)
    zone_manager = ZoneManagerSerializerOnlyName(read_only=True)
    asm = ASMSerializer(read_only=True)

    # Target fields (required)
    application_target = serializers.FloatField(required=True)
    pop_target = serializers.FloatField(required=True)
    esign_target = serializers.FloatField(required=True)
    new_taluk_target = serializers.FloatField(required=True)
    new_live_partners_target = serializers.FloatField(required=True)
    activations_target = serializers.FloatField(required=True)
    calls_target = serializers.FloatField(required=True)
    sd_collection_target = serializers.FloatField(required=True)

    # Achieved fields (default 0)
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
    def validate(self, attrs):
            """
            Custom validation:
            1. Ensure ASM belongs to the selected ZoneManager
            2. Ensure ZoneManager belongs to the logged-in user (optional)
            3. Prevent duplicate target for the same date
            """
            request = self.context.get('request')
            user = getattr(request, 'user', None)

            zone_manager = attrs.get('zone_manager')
            asm = attrs.get('asm')
            date = attrs.get('date')

            # Optional: Restrict ZoneManager to logged-in user
            # if user and zone_manager.user != user:
            #     raise serializers.ValidationError({
            #         "detail": "You can only create targets for your own ZoneManager."
            #     })

            # Ensure ASM belongs to ZoneManager
            if asm.zone_manager != zone_manager:
                raise serializers.ValidationError({
                    "detail": "ASM not found under your ZoneManager."
                })

            # Check for unique-together constraint: zone_manager + asm + date
            if ZMDailyTarget.objects.filter(zone_manager=zone_manager, asm=asm, date=date).exists():
                raise serializers.ValidationError({
                    "detail": "A target for this ZoneManager, ASM, and date already exists."
                })

            return attrs



from django.contrib.auth import get_user_model

User = get_user_model()

class ZoneManagerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',  'first_name', 'last_name']


class ZoneManagerBasicSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return {
            "id": obj.user.id,
          
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name
        }

    class Meta:
        model = ZoneManager
        fields = ['id', 'user']