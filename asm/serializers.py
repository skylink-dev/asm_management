# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from .models import ASM
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import authenticate

from rest_framework import serializers
from .models import ASM
from django.contrib.auth.models import User, Group
from zonemanager.models import ZoneManager
from master.models import State, District, Office


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


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





  # adjust import paths


class ASMSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    zone_manager = serializers.PrimaryKeyRelatedField(queryset=ZoneManager.objects.all(), required=False, allow_null=True)
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), required=False, allow_null=True)
    states = serializers.PrimaryKeyRelatedField(queryset=State.objects.all(), many=True, required=False)
    districts = serializers.PrimaryKeyRelatedField(queryset=District.objects.all(), many=True, required=False)
    offices = serializers.PrimaryKeyRelatedField(queryset=Office.objects.all(), many=True, required=False)

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

