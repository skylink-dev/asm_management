from django.db import models
from django.contrib.auth.models import User, Group
from master.models import State, District, Office, TargetCategory
from smart_selects.db_fields import ChainedManyToManyField
from django.utils import timezone

class ZoneManager(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="zone_manager"
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, null=True, blank=True, related_name="zone_managers"
    )

    states = models.ManyToManyField(
        State, blank=True, related_name="zone_managers"
    )

    districts = ChainedManyToManyField(
        District,
        chained_field="states",
        chained_model_field="state",
        blank=True,
        related_name="zone_managers"
    )

    offices = ChainedManyToManyField(
        Office,
        chained_field="districts",
        chained_model_field="district",
        blank=True,
        related_name="zone_managers"
    )

    def __str__(self):
        return self.user.username


class ZMDailyTarget(models.Model):
    zone_manager = models.ForeignKey(
        "ZoneManager",
        on_delete=models.SET_NULL,
        related_name="daily_targets",
        null=True,
        blank=True
    )
    asm = models.ForeignKey(
        "asm.ASM",
        on_delete=models.SET_NULL,
        related_name="zm_targets",
        null=True,
        blank=True
    )
    date = models.DateField(default=timezone.now, null=True, blank=True)

    # Each category as a separate field
    application_target = models.FloatField(default=0, null=True, blank=True)
    pop_target = models.FloatField(default=0, null=True, blank=True)
    esign_target = models.FloatField(default=0, null=True, blank=True)
    new_taluk_target = models.FloatField(default=0, null=True, blank=True)
    new_live_partners_target = models.FloatField(default=0, null=True, blank=True)
    activations_target = models.FloatField(default=0, null=True, blank=True)
    calls_target = models.FloatField(default=0, null=True, blank=True)
    sd_collection_target = models.FloatField(default=0, null=True, blank=True)

    # Achievement fields (optional, can track separately)
    application_achieve = models.FloatField(default=0, null=True, blank=True)
    pop_achieve = models.FloatField(default=0, null=True, blank=True)
    esign_achieve = models.FloatField(default=0, null=True, blank=True)
    new_taluk_achieve = models.FloatField(default=0, null=True, blank=True)
    new_live_partners_achieve = models.FloatField(default=0, null=True, blank=True)
    activations_achieve = models.FloatField(default=0, null=True, blank=True)
    calls_achieve = models.FloatField(default=0, null=True, blank=True)
    sd_collection_achieve = models.FloatField(default=0, null=True, blank=True)

    class Meta:
        unique_together = ("zone_manager", "asm", "date")
        ordering = ["-date"]

    def __str__(self):
        zm_name = f"{self.zone_manager.user.first_name} {self.zone_manager.user.last_name}" if self.zone_manager else "No ZM"
        asm_name = f"{self.asm.user.first_name} {self.asm.user.last_name}" if self.asm else "No ASM"
        return f"{zm_name} → {asm_name} ({self.date})"
