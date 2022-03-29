from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from courses.models import Courses
from users.models import CustomUser
from utils.response_utils import ResponseUtils
from .serializer import AssignmentSerializer
from .models import Assignments


class AssignmentView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AssignmentSerializer
    queryset = Assignments.objects.all()
    pagination_class = PageNumberPagination
    page_size = 10

    def list(self, request, *args, **kwargs):
        try:
            if request.user.is_superuser:
                self.queryset = Assignments.objects.all()
            else:
                self.queryset = Assignments.objects.filter(created_by_id=request.user.id)
            query_string_keys = list(request.GET.keys())

            # Get assignment by course
            if "course_id" in query_string_keys:
                self.queryset = self.queryset.filter(course_id=request.GET["course_id"])

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
            return ResponseUtils.failed_dependency({"data": [], "error": str(err)})

    def create(self, request, *args, **kwargs):
        try:
            serialized = self.get_serializer(data=request.data)
            if serialized.is_valid():
                user_obj = CustomUser.objects.get(id=request.user.id)
                if not request.data.get("course", ""):
                    return ResponseUtils.bad_request({"error": "Please provide course id"})
                course_obj = Courses.objects.get(id=request.data["course"])
                serialized.initial_data["course"] = course_obj
                assignment_obj = Assignments.objects.create(**serialized.initial_data)
                assignment_obj.created_by = user_obj
                assignment_obj.updated_by = user_obj

                assignment_obj.save()
                serialized_assignment = self.serializer_class(assignment_obj)
                return ResponseUtils.simple_response(serialized_assignment.data)
            else:
                return ResponseUtils.bad_request({"message": serialized.errors})
        except ObjectDoesNotExist as obj_err:
            return ResponseUtils.failed_dependency({"error": str(obj_err)})
        except Exception as err:
            return ResponseUtils.internal_server_error({"message": str(err)})

    def update(self, request, *args, **kwargs):
        response_data = {}
        try:
            assignment_id = request.data.get('assignment_id', '')
            if not assignment_id:
                data = {
                    "assignment_id": ["please provide assignment_id"]
                }
                return ResponseUtils.bad_request(data)

            # check if assignment belongs with current user
            assignment = Assignments.objects.get(id=assignment_id, created_by_id=request.user.id)
            if request.data.get("course", ""):
                assignment.course_id = request.data["course"]
            serializer = AssignmentSerializer(assignment, data=request.data)
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
                "message": "assignment does not exist or belongs to current user"
            }
            return ResponseUtils.failed_dependency(data)

        except Exception as err:
            response_data["error"] = str(err)
            return ResponseUtils.failed_dependency(response_data)


class AssignmentDetailView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AssignmentSerializer
    queryset = Assignments.objects.all()

    def get_detail(self, request, assignment_id):
        response_data = {
            "data": [],
            "error": ""
        }
        try:
            assignment = Assignments.objects.get(pk=assignment_id, created_by_id=request.user.id)
            serialized = self.serializer_class(assignment)
            response_data["data"] = serialized.data
            return ResponseUtils.simple_response(response_data)
        except ObjectDoesNotExist:
            response_data["error"] = "assignment does not exist in database"
            return ResponseUtils.not_found(response_data)
        except Exception as err:
            response_data["error"] = str(err)
            return ResponseUtils.not_found(response_data)

    def delete(self, request, assignment_id):
        response_data = {
            "data": [],
            "error": ""
        }
        try:
            assignment = Assignments.objects.get(pk=assignment_id, created_by_id=request.user.id)
            assignment.delete()
            response_data["data"] = assignment_id
            return ResponseUtils.simple_response(response_data)
        except ObjectDoesNotExist:
            response_data["error"] = "Assignment with this id does not exist"
            return ResponseUtils.not_found(response_data)
        except Exception as err:
            response_data["error"] = str(err)
            return ResponseUtils.not_found(response_data)
