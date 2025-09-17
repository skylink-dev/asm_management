# zonemanager/models.py
from django.db import models
from django.contrib.auth.models import User, Group
from master.models import State, District, Office
from smart_selects.db_fields import ChainedManyToManyField

class ZoneManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="zone_manager")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    
    # States (top-level)
    states = models.ManyToManyField(State, blank=True, related_name="zone_managers")
    
    # Districts chained to selected States
    districts = ChainedManyToManyField(
        District,
        chained_field="states",
        chained_model_field="state",
        blank=True,
        related_name="zone_managers"
    )
    
    # Offices chained to selected Districts
    offices = ChainedManyToManyField(
        Office,
        chained_field="districts",
        chained_model_field="district",
        blank=True,
        related_name="zone_managers"
    )

    def __str__(self):
        return self.user.username
