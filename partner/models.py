from django.db import models
from zonemanager.models import ZoneManager
from asm.models import ASM
from master.models import State, District, Office
from smart_selects.db_fields import ChainedManyToManyField
from django.utils import timezone


class Partner(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    zone_manager = models.ForeignKey(
        ZoneManager, on_delete=models.SET_NULL, null=True, blank=True, related_name="partners"
    )
    asm = models.ForeignKey(
        ASM, on_delete=models.SET_NULL, null=True, blank=True, related_name="partners"
    )

    # 🔹 States
    states = models.ManyToManyField(State, blank=True, related_name="partners")
    # 🔹 Districts chained to selected States
    districts = ChainedManyToManyField(
        District,
        chained_field="states",
        chained_model_field="state",
        blank=True,
        related_name="partners"
    )
    # 🔹 Offices chained to selected Districts
    offices = ChainedManyToManyField(
        Office,
        chained_field="districts",
        chained_model_field="district",
        blank=True,
        related_name="partners"
    )

    def __str__(self):
        return self.name

class SDCollection(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    partner = models.ForeignKey(
        'Partner',
        on_delete=models.CASCADE,
        related_name='sd_collections',
        null=True, blank=True,
        default=None
    )
    asm = models.ForeignKey(
        ASM,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        default=None
    )
    zone_manager = models.ForeignKey(
        ZoneManager,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        default=None
    )
    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    note = models.TextField(blank=True, null=True, default="")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_deleted = models.BooleanField(default=False)  # soft delete

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        partner_name = self.partner.name if self.partner else "Unknown Partner"
        return f"{partner_name} - {self.amount} on {self.date}"