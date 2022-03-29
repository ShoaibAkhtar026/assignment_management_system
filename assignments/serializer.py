from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Assignments
from users.serializers import UserCreateSerializer
from courses.serializer import CourseSerializer


class AssignmentSerializer(ModelSerializer):
    created_by = serializers.SerializerMethodField(source="get_created_by")
    course = serializers.SerializerMethodField(source="get_course")

    def get_created_by(self, obj):
        return UserCreateSerializer(obj.created_by, many=False).data

    def get_course(self, obj):
        return CourseSerializer(obj.course, many=False).data

    class Meta:
        model = Assignments
        fields = '__all__'
