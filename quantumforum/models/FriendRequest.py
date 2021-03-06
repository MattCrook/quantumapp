from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

# Status
# 0	Pending
# 1	Accepted
# 2	Declined
# 3	Blocked
# The action_user_id represent the id of the user who has performed the most recent status field update.

UserModel = get_user_model()

class FriendRequest(models.Model):

    sender_and_receiver = models.ForeignKey("Friendships", on_delete=models.CASCADE)
    status_code = models.ForeignKey("StatusCode", on_delete=models.CASCADE)
    last_updated_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    sent_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    class Meta:
        verbose_name = ("friend Request")
        verbose_name_plural = ("friend Requests")

    def __str__(self):
        return f'Last Updated By: {self.last_updated_by.first_name} {self.last_updated_by.last_name}'
