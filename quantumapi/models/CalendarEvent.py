from django.db import models
from quantumapi.models import User as QuantumUser




class CalendarEvent(models.Model):
    user = models.ForeignKey(QuantumUser, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    is_reminder_set = models.CharField(max_length=10, null=True, blank=True)
    reminder_value = models.CharField(max_length=30, null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)


    class Meta:
        verbose_name = ("calendar event")
        verbose_name_plural = ("calendar events")

    def __str__(self):
        return f'{self.title} -- {self.user.first_name} {self.user.last_name} -- {self.date}'
