import uuid as uuid
from django.db import models
from django.contrib.auth import get_user_model

from courses.models import Courses

User = get_user_model()


class Assignments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    name = models.CharField(max_length=500, unique=True, null=False, blank=False)
    description = models.CharField(max_length=500, null=True, blank=True)
    course = models.ForeignKey(Courses, related_name="assignment_course", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True, related_name="assignment_created_by",
                                   on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name="assignment_updated_by",
                                   on_delete=models.CASCADE)

    def __str__(self):
        return self.name
