from django.contrib.sites.models import Site, SiteManager
from django.db import models

class QuantumSite(Site, models.Model):
  def __init__(self, domain, name, objects):
    super().__init__(domain, name, objects)

    self.domain = domain
    self.name = name
    self.objects = SiteManager()

    class Meta:
        db_table = 'quantumappsite'
        verbose_name = ('quantumapisite')
        verbose_name_plural = ('quantumaposites')
        ordering = ['domain']

    def __str__(self):
        return self.domain

    def natural_key(self):
        return (self.domain,)
