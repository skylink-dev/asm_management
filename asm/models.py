from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User, Group

from asm_management import settings
from master.models import District, State, Taluk, Zone


# Create your models here.
#Model based on whether the user wants to set many roles and other details
# class Role(models.Model):
#     name = models.CharField(max_length=120)
#     isActive= models.CharField(max_length=120)
#
#
# class User(models.Model):
#     username = models.CharField()
#     password = models.CharField()
#     email = models.EmailField()
#     role= models.ForeignKey(Role, on_delete=models.CASCADE,default=list)
#
#     def __str__(self):
#         return self.username

class Role(models.Model):
    name = models.CharField(max_length=120)
    isActive= models.BooleanField(default=True)
    permission= models.ManyToManyField(Group, related_name="roles", )

    def __str__(self):
        return self.name


class ASM(models.Model):
    code = models.CharField(max_length=20, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role=models.ForeignKey(Role, on_delete=models.CASCADE, related_name="roles", )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users", )
    status = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    last_password_change = models.DateTimeField(auto_now=True)
    otp_allowed = models.BooleanField(default=False)
    otp_generated_time = models.DateTimeField(auto_now=True)
    otp_used = models.BooleanField(default=False)
    otp=models.CharField(max_length=20, unique=True, )

    def __str__(self):
        # shows both code + username for clarity
        return f"{self.code} - {self.user.username}"

class ASMTalukMapping(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20, unique=True, editable=False)
    asm_id = models.ForeignKey(ASM, on_delete=models.CASCADE, related_name="regions", )
    region_id =models.ForeignKey(Taluk, on_delete=models.CASCADE, related_name="regions", )

class ASMStateMapping(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20, unique=True, )
    asm_id = models.ForeignKey(ASM, on_delete=models.CASCADE, related_name="states", )
    state_id =models.ForeignKey(State, on_delete=models.CASCADE, related_name="states", )

class ASMZoneMapping(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20, unique=True, editable=False)
    asm_id = models.ForeignKey(ASM, on_delete=models.CASCADE, related_name="zones", )
    zone_id = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="zones",)

class ASMDistrictMapping(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20, unique=True, editable=False)
    asm_id = models.ForeignKey(ASM, on_delete=models.CASCADE, related_name="districts",)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, related_name="districts",)



# class PartnerCategories(models.Model):
#     id=models.AutoField(primary_key=True)
#     category_code=models.CharField(max_length=20, unique=True, default="S001")
#     category_name=models.CharField(max_length=20, unique=True, default="TEST")
#
#     class Meta:
#         verbose_name = "Partner Category"
#
# class Partner(models.Model):
#     id=models.AutoField(primary_key=True)
#     partner_code=models.CharField(max_length=20, unique=True, default="S001")
#     partner_name=models.CharField(max_length=20, unique=True, default="TEST")
#     user_id=models.ForeignKey(User, on_delete=models.CASCADE, related_name="users", default=1)
#     zone_id=models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="regions", default=1)
#     district_id=models.ForeignKey(District, on_delete=models.CASCADE, related_name="districts", default=1)
#     taluk_id=models.ForeignKey(Taluk, on_delete=models.CASCADE, related_name="talus", default=1)
#     status=models.BooleanField(default=False)
#     created_at=models.DateTimeField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)
#
#     class Meta:
#         verbose_name = "Partner"




