from django.db import models
# from django.forms.widgets import ClearableFileInput
import datetime


class NewsArticle(models.Model):

    date = models.DateTimeField(null=True, blank=True, default=datetime.datetime.utcnow)
    title = models.CharField(max_length=120, null=True, blank=True)
    type = models.CharField(max_length=60, null=True, blank=True)
    image = models.ImageField(blank=True, null=True)
    article = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = ("newsarticle")
        verbose_name_plural = ("newsarticles")

    def __str__(self):
        return f'Article: {self.article} -- {self.image}'
