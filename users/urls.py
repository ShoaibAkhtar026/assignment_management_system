from django.urls import path
from .views import UserCreateView, UserLoginView, UserLogOutView

urlpatterns = [
    path("register", UserCreateView.as_view()),
    path("login", UserLoginView.as_view()),
    path("logout", UserLogOutView.as_view()),
]
