from rest_framework import serializers

from users.models import CustomUser


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id',
                  'email',
                  'first_name',
                  'last_name',
                  'password',
                  'date_joined',
                  'created_at',
                  'updated_at',
                  ]


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
