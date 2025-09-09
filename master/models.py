from django.db import models

class Zone(models.Model):
    name = models.CharField(max_length=100, unique=True, default="Unknown Zone")
    code = models.CharField(max_length=20, unique=True, default="Z001")
    description = models.TextField(blank=True, null=True, default="No description")

    class Meta:
        verbose_name = "Zone"
        verbose_name_plural = "Zones"

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=100, unique=True, default="Unknown State")
    code = models.CharField(max_length=20, unique=True, default="S001")
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="states", default=1)
    description = models.TextField(blank=True, null=True, default="No description")

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100, default="Unknown District")
    code = models.CharField(max_length=20, default="D001")
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="districts", default=1)
    description = models.TextField(blank=True, null=True, default="No description")

    class Meta:
        unique_together = ('name', 'state')
        verbose_name = "District"
        verbose_name_plural = "Districts"

    def __str__(self):
        return self.name


class Taluk(models.Model):
    name = models.CharField(max_length=100, default="Unknown Taluk")
    code = models.CharField(max_length=20, default="T001")
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="taluks", default=1)
    description = models.TextField(blank=True, null=True, default="No description")

    class Meta:
        unique_together = ('name', 'district')
        verbose_name = "Taluk"
        verbose_name_plural = "Taluks"

    def __str__(self):
        return self.name
