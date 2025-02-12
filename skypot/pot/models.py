from django.db import models

# Create your models here.
class Database(models.Model):
    src_ip = models.GenericIPAddressField(db_index=True)
    lat = models.CharField(max_length=50)
    lon = models.CharField(max_length=50)
    country = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=200, blank=True, null=True)

class Credentials(models.Model):
    ip = models.ForeignKey(Database, on_delete=models.CASCADE, related_name="credentials")
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)