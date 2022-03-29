from django.urls import path
from courses.views import CourseView, CourseDetailView

urlpatterns = [
    path('', CourseView.as_view({'get': 'list', 'post': 'create', 'put': 'update'})),
    path('<str:course_id>', CourseDetailView.as_view({'get': 'get_detail', 'delete': 'delete'}))
]
