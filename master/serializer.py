from rest_framework import serializers
from .models import State, District, Office
from .models import TaskCategory

class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ['id', 'name', 'officetype', 'pincode', 'district']


class DistrictSerializer(serializers.ModelSerializer):
    offices = OfficeSerializer(many=True, read_only=True)  # nested offices under district

    class Meta:
        model = District
        fields = ['id', 'name', 'state', 'offices']


class StateSerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(many=True, read_only=True)  # nested districts under state

    class Meta:
        model = State
        fields = ['id', 'name', 'districts']



class TaskCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCategory
        fields = ['id', 'name', 'description']