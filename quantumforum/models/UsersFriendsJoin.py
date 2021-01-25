from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

# Status
# 0	Pending
# 1	Accepted
# 2	Declined
# 3	Blocked
# The action_user_id represent the id of the user who has performed the most recent status field update.




class Friendships(models.Model):
    UserModel = get_user_model()

    requester = models.ForeignKey("self", on_delete=models.CASCADE)
    addressee = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Friendship")
        verbose_name_plural = ("Friendships")
        unique_together = [("requester", "addressee")]

    def __str__(self):
        return f'Sent by: {self.requester.first_name} {self.requester.last_name}'


class StatusCode(models.Model):

    code = models.CharField(max_length=100, default=0)

    class Meta:
        verbose_name = ("Status Code")
        verbose_name_plural = ("Status Codes")

    def __str__(self):
        return f'Status Code: {self.code}'


class FriendRequest(models.Model):
    UserModel = get_user_model()

    sender_and_receiver = models.ForeignKey("Friendships", on_delete=models.CASCADE)
    status_code = models.ForeignKey("StatusCode", on_delete=models.CASCADE)
    last_updated_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("friend Request")
        verbose_name_plural = ("friend Requests")

    def __str__(self):
        return f'Last Updated By: {self.last_updated_by.first_name} {self.last_updated_by.last_name}'





# class FriendshipStatus(models.Model):
#     UserModel = get_user_model()

#     requester = models.ForeignKey(UserModel, on_delete=models.CASCADE)
#     addressee = models.ForeignKey(UserModel, on_delete=models.CASCADE)
#     status = models.ForeignKey("StatusCode", on_delete=models.CASCADE)
#     last_updated_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = ("Friendship Status")
#         verbose_name_plural = ("Friendship Statuses")
#         unique_together = [("requester", "addressee")]

#     def __str__(self):
#         return f'{self.requester.first_name}'

# class Friends(models.Model):
#     UserModel = get_user_model()

#     user = models.ForeignKey("self", related_name='self', on_delete=models.CASCADE)
#     friends = models.ManyToManyField(UserModel, through="Friendships",)

#     class Meta:
#         verbose_name = ("friend")
#         verbose_name_plural = ("friends")

#     def __str__(self):
#         return f'{self.code}'
