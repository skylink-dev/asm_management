
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    employee_id = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=3, null=True, blank=True)
    join_date = models.DateField(null=True, blank=True)
    avatar = models.URLField(default="https://via.placeholder.com/150?text=Avatar")
    department = models.CharField(max_length=120, default="Sales & Marketing")
    designation = models.CharField(max_length=120, default="Area Sales Manager")
    employee_status = models.CharField(max_length=20, default="Active")

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create profile automatically
        UserProfile.objects.create(user=instance, employee_id=f"EMP-{instance.id:04d}")
    else:
        # Save profile on user update
        if hasattr(instance, 'profile'):
            instance.profile.save()