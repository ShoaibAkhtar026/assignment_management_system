from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from users.models import CustomUser
from utils.response_utils import ResponseUtils
from .serializer import CourseSerializer
from .models import Courses


class CourseView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer
    queryset = Courses.objects.all()
    pagination_class = PageNumberPagination
    page_size = 10

    def list(self, request, *args, **kwargs):
        try:
            if request.user.is_superuser:
                self.queryset = Courses.objects.all()
            else:
                self.queryset = Courses.objects.filter(created_by_id=request.user.id)
            query_string_keys = list(request.GET.keys())

            # Return all records in case of page number is zero
            if 'page' in query_string_keys and request.GET['page'] == '0':
                serialized = self.serializer_class(self.queryset, many=True)
                return ResponseUtils.simple_response(serialized.data)

            page = self.paginate_queryset(self.queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serialized = self.serializer_class(self.queryset, many=True)
            return ResponseUtils.simple_response(serialized.data)
        except Exception as err:
            return ResponseUtils.internal_server_error({"data": [], "error": str(err)})

    def create(self, request, *args, **kwargs):
        try:
            serialized = self.get_serializer(data=request.data)
            if serialized.is_valid():
                user_obj = CustomUser.objects.get(id=request.user.id)
                course_obj = Courses.objects.create(**serialized.initial_data)
                course_obj.created_by = user_obj
                course_obj.updated_by = user_obj

                course_obj.save()
                serialized_course = self.serializer_class(course_obj)
                return ResponseUtils.simple_response(serialized_course.data)
            else:
                return ResponseUtils.bad_request({"message": serialized.errors})
        except Exception as err:
            return ResponseUtils.internal_server_error({"message": str(err)})

    def update(self, request, *args, **kwargs):
        response_data = {}
        try:
            course_id = request.data.get('course_id', '')
            if not course_id:
                data = {
                    "course_id": ["please provide course_id"]
                }
                return ResponseUtils.bad_request(data)

            # check if course belongs with current user
            assignment = Courses.objects.get(id=course_id, created_by_id=request.user.id)
            serializer = CourseSerializer(assignment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_data["data"] = serializer.data
                response_data["error"] = ""
                return ResponseUtils.simple_response(response_data)
            else:
                response_data["data"] = ""
                response_data["error"] = serializer.errors
                return ResponseUtils.bad_request(response_data)
        except ObjectDoesNotExist:
            data = {
                "message": "course does not exist or belongs to current user"
            }
            return ResponseUtils.failed_dependency(data)

        except Exception as err:
            response_data["error"] = str(err)
            return ResponseUtils.failed_dependency(response_data)


class CourseDetailView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer
    queryset = Courses.objects.all()

    def get_detail(self, request, course_id):
        response_data = {
            "data": [],
            "error": ""
        }
        try:
            course = Courses.objects.get(pk=course_id, created_by_id=request.user.id)
            serialized = self.serializer_class(course)
            response_data["data"] = serialized.data
            return ResponseUtils.simple_response(response_data)
        except ObjectDoesNotExist:
            response_data["error"] = "course does not exist"
            return ResponseUtils.not_found(response_data)
        except Exception as err:
            response_data["error"] = str(err)
            return ResponseUtils.not_found(response_data)

    def delete(self, request, course_id):
        response_data = {
            "data": [],
            "error": ""
        }
        try:
            course = Courses.objects.get(pk=course_id, created_by_id=request.user.id)
            course.delete()
            response_data["data"] = course_id
            return ResponseUtils.simple_response(response_data)
        except ObjectDoesNotExist:
            response_data["error"] = "Course with this id does not exist"
            return ResponseUtils.not_found(response_data)
        except Exception as err:
            response_data["error"] = str(err)
            return ResponseUtils.not_found(response_data)
