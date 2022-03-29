from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.serializers import UserCreateSerializer
from .models import Courses


class CourseSerializer(ModelSerializer):
    created_by = serializers.SerializerMethodField(source="get_created_by")

    def get_created_by(self, obj):
        return UserCreateSerializer(obj.created_by, many=False).data

    class Meta:
        model = Courses
        fields = '__all__'
