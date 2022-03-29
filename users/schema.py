import graphene
from graphene_django.types import DjangoObjectType
from .models import CustomUser


class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ("id", "first_name", "last_name", "email")


class UserQuery(graphene.ObjectType):
    all_users = graphene.List(UserType)

    def resolve_users(self, info, **kwargs):
        return CustomUser.objects.all()
