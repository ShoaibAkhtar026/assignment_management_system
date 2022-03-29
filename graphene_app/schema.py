import graphene
from users.schema import UserQuery


# class Mutations:
#     pass


class Query(UserQuery):
    pass


schema = graphene.Schema(query=Query, types=[])
