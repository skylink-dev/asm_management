from django.db import models
from django.contrib.auth.models import User, Group
from master.models import State, District, Office
from zonemanager.models import ZoneManager, ZMDailyTarget
from smart_selects.db_fields import ChainedManyToManyField
from django.utils import timezone


class Role(models.Model):
    name = models.CharField(max_length=120, default="Unnamed")
    isActive = models.BooleanField(default=True)
    permission = models.ManyToManyField(Group, related_name="roles", blank=True)

    def __str__(self):
        return self.name


class ASM(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.SET_NULL, related_name="asm", null=True, blank=True, default=None
    )
    zone_manager = models.ForeignKey(
        ZoneManager,
        on_delete=models.SET_NULL,
        related_name="asms",
        null=True,
        blank=True,
        default=None
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, related_name="asms", null=True, blank=True, default=None
    )

    # States
    states = models.ManyToManyField(State, blank=True, related_name="asms")
    
    # Districts chained to selected States
    districts = ChainedManyToManyField(
        District,
        chained_field="states",
        chained_model_field="state",
        blank=True,
        related_name="asms"
    )
    
    # Offices chained to selected Districts
    offices = ChainedManyToManyField(
        Office,
        chained_field="districts",
        chained_model_field="district",
        blank=True,
        related_name="asms"
    )

    def __str__(self):
        if self.user:
            zm_name = self.zone_manager.user.username if self.zone_manager and self.zone_manager.user else "No ZM"
            return f"{self.user.username} ({zm_name})"
        return "Unnamed ASM"


class ASMDailyTarget(models.Model):
    asm = models.ForeignKey(
        ASM, on_delete=models.SET_NULL, related_name="daily_targets", null=True, blank=True, default=None
    )
    zm_daily_target = models.ForeignKey(
        ZMDailyTarget, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    date = models.DateField(default=timezone.now)

    # Targets
    application_target = models.FloatField(default=0)
    pop_target = models.FloatField(default=0)
    esign_target = models.FloatField(default=0)
    new_taluk_target = models.FloatField(default=0)
    new_live_partners_target = models.FloatField(default=0)
    activations_target = models.FloatField(default=0)
    calls_target = models.FloatField(default=0)
    sd_collection_target = models.FloatField(default=0)

    # Achievements
    application_achieve = models.FloatField(default=0)
    pop_achieve = models.FloatField(default=0)
    esign_achieve = models.FloatField(default=0)
    new_taluk_achieve = models.FloatField(default=0)
    new_live_partners_achieve = models.FloatField(default=0)
    activations_achieve = models.FloatField(default=0)
    calls_achieve = models.FloatField(default=0)
    sd_collection_achieve = models.FloatField(default=0)

    class Meta:
        unique_together = ("asm", "date")
        ordering = ["-date"]

    def __str__(self):
        asm_name = self.asm.user.get_full_name() if self.asm and self.asm.user else "Unnamed ASM"
        return f"{asm_name} ({self.date})"
