from django.urls import path
from assignments.views import AssignmentView, AssignmentDetailView

urlpatterns = [
    path('', AssignmentView.as_view({'get': 'list', 'post': 'create', 'put': 'update'})),
    path('<str:assignment_id>', AssignmentDetailView.as_view({'get': 'get_detail', 'delete': 'delete'}))
]
