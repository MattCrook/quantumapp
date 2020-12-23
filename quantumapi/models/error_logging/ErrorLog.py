import json
from quantumapi.models import User as UserModel
from django.db import models
from django.utils import timezone

class ErrorLog(models.Model):
    user = models.ForeignKey(UserModel, null=True, blank=True, on_delete=models.CASCADE)
    environment = models.TextField(null=True, blank=True)
    error_message = models.CharField(max_length=400, null=True, blank=True)
    stack = models.TextField(null=True, blank=True)
    component = models.CharField(max_length=100, null=True, blank=True)
    calling_function = models.CharField(max_length=100, null=True, blank=True)
    key = models.TextField(null=True, blank=True)
    session = models.TextField(null=True, blank=True)
    request_data = models.TextField(null=True, blank=True)
    headers = models.TextField(null=True, blank=True)
    host_ip = models.TextField(null=True, blank=True)
    date = models.DateTimeField()

    class Meta:
        verbose_name = ("error log")
        verbose_name_plural = ("error logs")
        ordering = ("user", )

    def __str__(self):
        return f'{self.user.email} -- {self.error_message} -- {self.date}'
