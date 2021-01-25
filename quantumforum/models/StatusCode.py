from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

# Status
# 0	Pending
# 1	Accepted
# 2	Declined
# 3	Blocked
# The action_user_id represent the id of the user who has performed the most recent status field update.

class StatusCode(models.Model):

    code = models.CharField(max_length=2, default=0)
    description = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = ("Status Code")
        verbose_name_plural = ("Status Codes")

    def __str__(self):
        return f'Status Code: {self.code}'
