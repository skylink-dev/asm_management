from django.contrib.auth import authenticate


from asm.models import ASM
from django.contrib.auth.models import User, Group


from rest_framework import serializers
from django.contrib.auth.models import User

from zonemanager.serializers import ZoneManagerSerializer
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    """Nested serializer for basic User info"""
    full_name = serializers.SerializerMethodField()
    groups = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name','groups']

    def get_full_name(self, obj):
        return obj.get_full_name()


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Nested user info
    zone = ZoneManagerSerializer(source="user.zone_manager", read_only=True)
    class Meta:
        model = UserProfile
        fields = [
            'user',
            'zone',
            'employee_id',
            'phone',
            'address',
            'date_of_birth',
            'blood_group',
            'join_date',
            'avatar',
            'department',
            'designation',
            'employee_status'
        ]







class UploadFileSerializer(serializers.Serializer):
    file = serializers.FileField()


class ASMRegisterSerializer(serializers.ModelSerializer):
    # User fields
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        model = ASM
        fields = [
            "username", "password", "first_name", "last_name",   # User
            "zone_manager", "group", "states", "districts", "offices",  # ASM
            "email", "mobile", "otp_allowed"
        ]


    def create(self, validated_data):
        # Extract user fields
        username = validated_data.pop("username")
        password = validated_data.pop("password")
        first_name = validated_data.pop("first_name", "")
        last_name = validated_data.pop("last_name", "")

        # Extract M2M fields (remove them before ASM create)
        states = validated_data.pop("states", [])
        districts = validated_data.pop("districts", [])
        offices = validated_data.pop("offices", [])

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {"username": f"Username '{username}' already exists."}
            )

        # Create User
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        # Create ASM (without M2M)
        asm = ASM.objects.create(user=user, **validated_data)

        # Assign ManyToMany
        if states:
            asm.states.set(states)
        if districts:
            asm.districts.set(districts)
        if offices:
            asm.offices.set(offices)

        return asm



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            raise serializers.ValidationError("Both username and password are required.")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or password.")

        if not user.is_active:
            raise serializers.ValidationError("This account is inactive. Please contact admin.")

        data["user"] = user
        return data
