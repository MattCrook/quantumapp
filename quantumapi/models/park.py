from django.db import models
from django.db.models import F



class Park(models.Model):

    name = models.CharField(max_length=50)
    parkLocation = models.CharField(max_length=50)
    parkCountry = models.CharField(max_length=50)


    class Meta:
        verbose_name = ("park")
        verbose_name_plural = ("parks")
        ordering = ("name", )


    def __str__(self):
        return f'{self.name} -- {self.parkLocation} -- {self.parkCountry}'
