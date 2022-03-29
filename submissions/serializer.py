from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.serializers import UserCreateSerializer
from .models import Submissions
from assignments.serializer import AssignmentSerializer


class SubmissionSerializer(ModelSerializer):
    assignment = serializers.SerializerMethodField(source="get_assignment")
    created_by = serializers.SerializerMethodField(source="get_created_by")

    def get_assignment(self, obj):
        return AssignmentSerializer(obj.assignment, many=False).data

    def get_created_by(self, obj):
        return UserCreateSerializer(obj.created_by, many=False).data

    class Meta:
        model = Submissions
        fields = '__all__'
