from django.db import models

class Zone(models.Model):
    name = models.CharField(max_length=100, unique=True, default="Default Zone")
    code = models.CharField(max_length=20, unique=True, default="ZONE001")
    description = models.TextField(blank=True, null=True, default="No description available")

    class Meta:
        verbose_name = "Zone"
        verbose_name_plural = "Zones"

    def __str__(self):
        return self.name
