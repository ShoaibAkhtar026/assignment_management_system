
from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView
from graphene_app.schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('assignment/', include('assignments.urls')),
    path('course/', include('courses.urls')),
    path('submission/', include('submissions.urls')),
    path('graphql', GraphQLView.as_view(graphiql=True, schema=schema))
]
