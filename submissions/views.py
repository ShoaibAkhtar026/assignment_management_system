from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from assignments.models import Assignments
from courses.models import Courses
from users.models import CustomUser
from utils.response_utils import ResponseUtils
from .serializer import SubmissionSerializer
from .models import Submissions


class SubmissionView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionSerializer
    queryset = Submissions.objects.all()
    pagination_class = PageNumberPagination
    page_size = 10

    def list(self, request, *args, **kwargs):
        try:
            if request.user.is_superuser:
                self.queryset = Submissions.objects.all()
            else:
                self.queryset = Submissions.objects.filter(created_by_id=request.user.id)
            query_string_keys = list(request.GET.keys())

            # get all submissions for an assignment
            if "assignment_id" in query_string_keys:
                self.queryset = self.queryset.filter(assignment_id=request.GET["assignment_id"])

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
                if not request.data.get("assignment", ""):
                    return ResponseUtils.bad_request({"error": "Please provide assignment id"})
                assignment_obj = Assignments.objects.get(id=request.data["assignment"])
                serialized.initial_data["assignment"] = assignment_obj
                submission_obj = Submissions.objects.create(**serialized.initial_data)
                submission_obj.created_by = user_obj
                submission_obj.updated_by = user_obj

                submission_obj.save()
                serialized_submission = self.serializer_class(submission_obj)
                return ResponseUtils.simple_response(serialized_submission.data)
            else:
                return ResponseUtils.bad_request({"message": serialized.errors})
        except ObjectDoesNotExist as obj_err:
            return ResponseUtils.failed_dependency({"error": str(obj_err)})
        except Exception as err:
            return ResponseUtils.internal_server_error({"message": str(err)})

    def update(self, request, *args, **kwargs):
        response_data = {}
        try:
            submission_id = request.data.get('submission_id', '')
            if not submission_id:
                data = {
                    "submission_id": ["please provide submission_id"]
                }
                return ResponseUtils.bad_request(data)

            # check if submission belongs with current user
            submission = Submissions.objects.get(id=submission_id, created_by_id=request.user.id)
            if request.data.get("assignment", ""):
                submission.assignment_id = request.data["assignment"]
            serializer = SubmissionSerializer(submission, data=request.data)
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
                "message": "submission does not exist or belongs to current user"
            }
            return ResponseUtils.failed_dependency(data)

        except Exception as err:
            response_data["error"] = str(err)
            return ResponseUtils.failed_dependency(response_data)


class SubmissionDetailView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionSerializer
    queryset = Submissions.objects.all()

    def get_detail(self, request, submission_id):
        response_data = {
            "data": [],
            "error": ""
        }
        try:
            submission = Submissions.objects.get(pk=submission_id, created_by_id=request.user.id)
            serialized = self.serializer_class(submission)
            response_data["data"] = serialized.data
            return ResponseUtils.simple_response(response_data)
        except ObjectDoesNotExist:
            response_data["error"] = "submission does not exist in database"
            return ResponseUtils.not_found(response_data)
        except Exception as err:
            response_data["error"] = str(err)
            return ResponseUtils.not_found(response_data)

    def delete(self, request, submission_id):
        response_data = {
            "data": [],
            "error": ""
        }
        try:
            submission = Submissions.objects.get(pk=submission_id, created_by_id=request.user.id)
            submission.delete()
            response_data["data"] = submission_id
            return ResponseUtils.simple_response(response_data)
        except ObjectDoesNotExist:
            response_data["error"] = "Submission with this id does not exist"
            return ResponseUtils.not_found(response_data)
        except Exception as err:
            response_data["error"] = str(err)
            return ResponseUtils.not_found(response_data)
