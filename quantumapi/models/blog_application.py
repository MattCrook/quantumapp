from django.db import models
from quantumapi.models import User as QuantumUser




class BlogContributorApplication(models.Model):
    user = models.ForeignKey(QuantumUser, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    social_media = models.CharField(max_length=100, null=True, blank=True)
    short_description = models.TextField(max_length=300, null=True, blank=True)
    date_submitted = models.DateTimeField()

    class Meta:
        verbose_name = ("blogcontributorapplication")
        verbose_name_plural = ("blogcontributorapplications")

    def __str__(self):
        return f'Article: {self.article} -- {self.image}'
