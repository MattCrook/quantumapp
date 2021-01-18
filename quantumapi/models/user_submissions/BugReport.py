from django.db import models
from quantumapi.models import User as QuantumUser

class BugReport(models.Model):
    title = models.CharField(max_length=300, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField()
    user = models.ForeignKey(QuantumUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("bug report")
        verbose_name_plural = ("bug reports")

    def __str__(self):
        return f'{self.title} -- {self.description}'
