from django.db import models
from django.contrib.auth.models import User
from master.models import State, District, Office
from zonemanager.models import ZoneManager
from asm.models import ASM
from smart_selects.db_fields import ChainedManyToManyField

class Partner(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)

    zone_manager = models.ForeignKey(ZoneManager, on_delete=models.SET_NULL, null=True, blank=True)
    asm = models.ForeignKey(ASM, on_delete=models.SET_NULL, null=True, blank=True)

    # 🔹 States
    states = models.ManyToManyField(State, blank=True, related_name="partners")
    # 🔹 Districts chained to selected States
    districts = ChainedManyToManyField(District, chained_field="states", chained_model_field="state", blank=True, related_name="partners")
    # 🔹 Offices chained to selected Districts
    offices = ChainedManyToManyField(Office, chained_field="districts", chained_model_field="district", blank=True, related_name="partners")

    def __str__(self):
        return self.name
