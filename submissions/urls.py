from django.urls import path
from submissions.views import SubmissionView, SubmissionDetailView

urlpatterns = [
    path('', SubmissionView.as_view({'get': 'list', 'post': 'create', 'put': 'update'})),
    path('<str:submission_id>', SubmissionDetailView.as_view({'get': 'get_detail', 'delete': 'delete'}))
]
