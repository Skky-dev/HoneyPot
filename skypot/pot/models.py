from django.db import models

# Create your models here.
class Database(models.Model):
    src_ip = models.GenericIPAddressField(db_index=True)
    lat = models.CharField(max_length=50)
    lon = models.CharField(max_length=50)
    country = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=200, blank=True, null=True)