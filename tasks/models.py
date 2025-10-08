from django.db import models
from django.utils import timezone
from asm.models import ASM
from zonemanager.models import ZoneManager
from master.models import TaskCategory

class ASMTask(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('hold', 'Hold'),
    )

    zone_manager = models.ForeignKey(
        ZoneManager,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks"
    )
    asm = models.ForeignKey(
        ASM,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    category = models.ForeignKey(
        TaskCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks"
    )
    title = models.CharField(max_length=255)
    details = models.TextField(default="No details provided")
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    # ✅ Soft delete field
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_date", "-created_at"]

    def __str__(self):
        asm_name = self.asm.user.get_full_name() if self.asm else "No ASM"
        category_name = self.category.name if self.category else "No Category"
        return f"{asm_name} | {category_name} | {self.status}"
