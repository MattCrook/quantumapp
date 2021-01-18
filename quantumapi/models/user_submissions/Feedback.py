from django.db import models
from quantumapi.models import User as QuantumUser


class Feedback(models.Model):
    subject = models.CharField(max_length=400, null=True, blank=True)
    feedback = models.CharField(max_length=1000, null=True, blank=True)
    date = models.DateTimeField()
    user = models.ForeignKey(QuantumUser, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("feedback")
        verbose_name_plural = ("feedback Submissions")

    def __str__(self):
        return f'{self.subject} -- {self.feedback}'
