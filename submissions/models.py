import uuid as uuid
from django.db import models
from django.contrib.auth import get_user_model

from assignments.models import Assignments

User = get_user_model()


class Submissions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    assignment = models.ForeignKey(Assignments, related_name="assignment_course", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True, related_name="submission_created_by",
                                   on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, blank=True, related_name="submission_updated_by",
                                   on_delete=models.CASCADE)

    def __str__(self):
        return self.assignment
