from django.db import models
from django.contrib.auth.models import User, Group

from master.models import State, District, Office
from zonemanager.models import ZoneManager
from smart_selects.db_fields import ChainedManyToManyField
from zonemanager.models import ZMDailyTarget
from django.utils import timezone

class Role(models.Model):
    name = models.CharField(max_length=120)
    isActive= models.BooleanField(default=True)
    permission= models.ManyToManyField(Group, related_name="roles", )

    def __str__(self):
        return self.name



class ASM(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="asm"
    )
    zone_manager = models.ForeignKey(
        "zonemanager.ZoneManager",  # Use string reference to avoid circular import
        on_delete=models.CASCADE,
        related_name="asms",
        null=True,
        blank=True
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, null=True, blank=True, related_name="asms"
    )

    # 🔹 States (top-level)
    states = models.ManyToManyField(
        State, blank=True, related_name="asms"
    )

    # 🔹 Districts chained to selected States
    districts = ChainedManyToManyField(
        District,
        chained_field="states",
        chained_model_field="state",
        blank=True,
        related_name="asms"
    )

    # 🔹 Offices chained to selected Districts
    offices = ChainedManyToManyField(
        Office,
        chained_field="districts",
        chained_model_field="district",
        blank=True,
        related_name="asms"
    )
    # email = models.EmailField(null=True, blank=True)
    # mobile = models.CharField(max_length=10, null=True, blank=True)
    # isActive = models.BooleanField(default=True)
    # last_login = models.DateTimeField(auto_now=True)
    # last_password_change = models.DateTimeField(auto_now=True)
    # otp_allowed = models.BooleanField(default=False)
    # otp_generated_time = models.DateTimeField(auto_now=True)
    # otp_used = models.BooleanField(default=False)
    # otp = models.CharField(default="", null=True, blank=True)


def __str__(self):
        return f"{self.user.username} ({self.zone_manager.user.username})"


class ASMDailyTarget(models.Model):
    asm = models.ForeignKey("ASM", on_delete=models.CASCADE, related_name="daily_targets")
    zm_daily_target = models.ForeignKey(ZMDailyTarget, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(default=timezone.now)

    # Targets
    application_target = models.FloatField(default=0, null=True, blank=True)
    pop_target = models.FloatField(default=0, null=True, blank=True)
    esign_target = models.FloatField(default=0, null=True, blank=True)
    new_taluk_target = models.FloatField(default=0, null=True, blank=True)
    new_live_partners_target = models.FloatField(default=0, null=True, blank=True)
    activations_target = models.FloatField(default=0, null=True, blank=True)
    calls_target = models.FloatField(default=0, null=True, blank=True)
    sd_collection_target = models.FloatField(default=0, null=True, blank=True)

    # Achievements
    application_achieve = models.FloatField(default=0, null=True, blank=True)
    pop_achieve = models.FloatField(default=0, null=True, blank=True)
    esign_achieve = models.FloatField(default=0, null=True, blank=True)
    new_taluk_achieve = models.FloatField(default=0, null=True, blank=True)
    new_live_partners_achieve = models.FloatField(default=0, null=True, blank=True)
    activations_achieve = models.FloatField(default=0, null=True, blank=True)
    calls_achieve = models.FloatField(default=0, null=True, blank=True)
    sd_collection_achieve = models.FloatField(default=0, null=True, blank=True)

    class Meta:
        unique_together = ("asm", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.asm.user.get_full_name()} ({self.date})"