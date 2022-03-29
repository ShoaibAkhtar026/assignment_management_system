import datetime
import pytz

from django.contrib.auth import authenticate, logout
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import CustomUser
from users.serializers import UserCreateSerializer, UserLoginSerializer
from utils.response_utils import ResponseUtils


class UserCreateView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer

    def post(self, request):
        try:
            serialized_data = self.serializer_class(data=request.data)
            if serialized_data.is_valid():
                first_name = request.data.get('first_name', '')
                last_name = request.data.get('last_name', '')
                email = request.data.get('email', '')
                password = request.data.get('password', '')

                user = CustomUser.objects.create(
                    first_name=first_name, last_name=last_name, email=email, date_joined=datetime.datetime.now(pytz.utc))
                user.set_password(password)
                user.save()
                data = UserCreateSerializer(user).data
                return ResponseUtils.simple_response(data)
            else:
                return ResponseUtils.bad_request({"message": serialized_data.errors})

        except Exception as e:
            return ResponseUtils.bad_request({"message": str(e)})


class UserLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        try:
            serialized_data = self.serializer_class(data=request.data)
            if serialized_data.is_valid():
                email = request.data.get('email', '')
                password = request.data.get('password', '')
                user = authenticate(username=email, password=password)
                if user is not None:
                    return ResponseUtils.simple_response({"message": "Successfully Logged In"})
                else:
                    return ResponseUtils.unauthorized({"message": "Email/password is not correct"})
            else:
                return ResponseUtils.bad_request({"message": serialized_data.errors})

        except Exception as e:
            return ResponseUtils.internal_server_error({"message": str(e)})


class UserLogOutView(APIView):

    def post(self, request):
        try:
            logout(request)
            return ResponseUtils.simple_response({"message": "Successfully Logged Out"})

        except Exception as e:
            return ResponseUtils.internal_server_error({"message": str(e)})
