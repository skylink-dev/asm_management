# serializers.py
from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password

from .models import ASM
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import authenticate

from .models import ASM
from django.contrib.auth.models import User, Group
from zonemanager.models import ZoneManager
from master.models import State, District, Office


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ["id", "name"]

# District serializer with nested offices (id and name only)
class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = ["id", "name"]

# State serializer with nested districts (id and name only)
class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = ["id", "name"]

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), write_only=True)
    role_info = GroupSerializer(source='role', read_only=True)  # Add role info in response
    code = serializers.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'role', 'role_info', 'code']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "Username already exists."})

        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists."})

        if ASM.objects.filter(code=attrs['code']).exists():
            raise serializers.ValidationError({"code": "ASM code already exists."})

        return attrs

    def create(self, validated_data):
        # Remove extra fields
        password2 = validated_data.pop('password2')
        role = validated_data.pop('role')
        code = validated_data.pop('code')

        # Create User
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])
        user.save()

        # Add user to the selected group/role
        user.groups.add(role)

        # Create ASM
        asm = ASM.objects.create(
            user=user,
            role=role,
            code=code,
            status=True
        )

        return user


class ASMUserSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    role = GroupSerializer(read_only=True)  # Use GroupSerializer for role
    user_details = serializers.SerializerMethodField()
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = ASM
        fields = ['id', 'code', 'user', 'user_id', 'role', 'status', 'created_at', 'updated_at', 'user_details']


    @staticmethod
    def get_user_details(self, obj):
        return {
            'username': obj.user.username,
            'email': obj.user.email,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'is_active': obj.user.is_active,
            'date_joined': obj.user.date_joined
        }


# Additional serializer for user update
class UserUpdateSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role']


class ASMUpdateSerializer(serializers.ModelSerializer):
    user_data = UserUpdateSerializer(source='user', required=False)

    class Meta:
        model = ASM
        fields = ['code', 'status', 'user_data']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user_data', None)

        # Update ASM fields
        instance.code = validated_data.get('code', instance.code)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        # Update User fields if provided
        if user_data:
            user = instance.user
            role = user_data.pop('role', None)

            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.email = user_data.get('email', user.email)
            user.save()

            # Update role if provided
            if role:
                # Clear existing groups and add new role
                user.groups.clear()
                user.groups.add(role)
                instance.role = role
                instance.save()

        return instance


# Serializer for listing available roles/groups
class RoleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class ASMLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Authenticate the user
            user = authenticate(request=self.context.get('request'),username=username, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')

            # Check if user has an ASM profile
            try:
                asm_profile = ASM.objects.get(user=user)
                if not asm_profile.status:
                    raise serializers.ValidationError(
                        _('Your account is deactivated. Please contact administrator.'),
                        code='authorization'
                    )
            except ASM.DoesNotExist:
                raise serializers.ValidationError(
                    _('No ASM profile found for this user.'),
                    code='authorization'
                )

            attrs['user'] = user
            attrs['asm'] = asm_profile
            return attrs

        raise serializers.ValidationError(
            _('Must include "email" and "password".'),
            code='authorization'
        )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class ZoneManagerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ZoneManager
        fields = ["id", "user"]

  # adjust import paths
class GroupForRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]

class ASMSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    zone_manager = ZoneManagerSerializer(read_only=True)
    group = GroupSerializer(read_only=True)
    states = StateSerializer(many=True, read_only=True)
    districts = DistrictSerializer(many=True, read_only=True)
    offices = OfficeSerializer(many=True, read_only=True)

    class Meta:
        model = ASM
        fields = [
            "id",
            "user",
            "zone_manager",
            "group",
            "states",
            "districts",
            "offices",
        ]



class ASMSerializerByZonalManager(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    group = GroupSerializer(read_only=True)
    states = StateSerializer(many=True, read_only=True)
    districts = DistrictSerializer(many=True, read_only=True)
    offices = OfficeSerializer(many=True, read_only=True)

    class Meta:
        model = ASM
        fields = [
            "id",
            "user",
            "group",
            "states",
            "districts",
            "offices",
        ]




#Arul update
from zonemanager.serializers import ZoneManagerSerializerOnlyName
from .models import ZMDailyTarget
from asm.serializers import ASMSerializer
from zonemanager.serializers import ZoneManagerSerializerOnlyName
from .models import ASMDailyTarget
class ASMDailyTargetSerializer(serializers.ModelSerializer):
    asm = ASMSerializer(read_only=True)
    zm_daily_target = serializers.PrimaryKeyRelatedField(read_only=True)
    target_flag = serializers.IntegerField(write_only=True, required=False)
    achieve_flag = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = ASMDailyTarget
        fields = "__all__"

    def validate(self, attrs):
        request = self.context.get("request")
        asm = getattr(request.user, "asm", None)
        if not asm:
            raise serializers.ValidationError({"message": "ASM profile not found for user."})

        date = attrs.get("date")
        if not date:
            raise serializers.ValidationError({"message": "Date is required."})

        target_flag = attrs.get("target_flag", 0)
        achieve_flag = attrs.get("achieve_flag", 0)

        # If adding target, ensure no duplicate date
        if target_flag == 1 and ASMDailyTarget.objects.filter(asm=asm, date=date).exists():
            raise serializers.ValidationError({"message": "Target already set for this date."})

        attrs["asm"] = asm
        return attrs

    def create(self, validated_data):
        target_flag = validated_data.pop("target_flag", 0)
        achieve_flag = validated_data.pop("achieve_flag", 0)
        asm = validated_data["asm"]
        date = validated_data["date"]

        # 1️⃣ If target_flag=1 → Create new or update target fields
        if target_flag == 1:
            instance, created = ASMDailyTarget.objects.get_or_create(asm=asm, date=date)
            for field in [
                "application_target", "pop_target", "esign_target", "new_taluk_target",
                "new_live_partners_target", "activations_target", "calls_target", "sd_collection_target"
            ]:
                if field in validated_data:
                    setattr(instance, field, validated_data[field])
            instance.save()
            return instance

        # 2️⃣ If achieve_flag=1 → Update ASM achievements AND ZM target achievements
        elif achieve_flag == 1:
            try:
                # Update ASM Daily Target
                instance = ASMDailyTarget.objects.get(asm=asm, date=date)
            except ASMDailyTarget.DoesNotExist:
                raise serializers.ValidationError({"message": "Target not found for this date."})

            # Update ASM achievement fields
            achievement_fields = [
                "application_achieve", "pop_achieve", "esign_achieve", "new_taluk_achieve",
                "new_live_partners_achieve", "activations_achieve", "calls_achieve", "sd_collection_achieve"
            ]
            for field in achievement_fields:
                if field in validated_data:
                    setattr(instance, field, validated_data[field])
            instance.save()

            # Also update ZMDailyTarget achievement fields if linked
            if instance.zm_daily_target:
                zm_instance = instance.zm_daily_target
                for field in achievement_fields:
                    # Directly map ASM achievement fields to ZM achievement fields
                    if hasattr(zm_instance, field) and field in validated_data:
                        setattr(zm_instance, field, validated_data[field])
                zm_instance.save()

            return instance

        raise serializers.ValidationError({"message": "Either target_flag or achieve_flag must be 1."})

        

        

        
    

class ASMDailyTargetListSerializer(serializers.ModelSerializer):
    zm_targets = serializers.SerializerMethodField()

    class Meta:
        model = ASMDailyTarget
        fields = [
            "id", "date",
            "application_target", "pop_target", "esign_target",
            "new_taluk_target", "new_live_partners_target",
            "activations_target", "calls_target", "sd_collection_target",

            "application_achieve", "pop_achieve", "esign_achieve",
            "new_taluk_achieve", "new_live_partners_achieve",
            "activations_achieve", "calls_achieve", "sd_collection_achieve",

            "zm_targets"
        ]

    def get_zm_targets(self, obj):
        zm_data = {}
        if obj.zm_daily_target:
            zm = obj.zm_daily_target
            zm_data = {
                "application_target": zm.application_target,
                "pop_target": zm.pop_target,
                "esign_target": zm.esign_target,
                "new_taluk_target": zm.new_taluk_target,
                "new_live_partners_target": zm.new_live_partners_target,
                "activations_target": zm.activations_target,
                "calls_target": zm.calls_target,
                "sd_collection_target": zm.sd_collection_target,
            }
        return zm_data
    

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


