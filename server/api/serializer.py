from rest_framework import serializers
from .models import User, SMModel, Project


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}


class SMModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMModel
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
