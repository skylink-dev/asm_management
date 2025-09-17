from django.db import models


class PincodeData(models.Model):
    circlename = models.CharField(max_length=100, default="", blank=True)
    regionname = models.CharField(max_length=100, default="", blank=True)
    divisionname = models.CharField(max_length=100, default="", blank=True)
    officename = models.CharField(max_length=150, default="", blank=True)
    pincode = models.CharField(max_length=10, default="", blank=True)
    officetype = models.CharField(max_length=50, default="", blank=True)
    delivery = models.CharField(max_length=50, default="", blank=True)
    district = models.CharField(max_length=100, default="", blank=True)
    statename = models.CharField(max_length=100, default="", blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)


    def __str__(self):
        return f"{self.officename} ({self.pincode})"





# State
class State(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# District under State
class District(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="districts")

    class Meta:
        unique_together = ("name", "state")  # Avoid duplicate districts per state

    def __str__(self):
        return f"{self.name} ({self.state.name})"


# Office/Taluk under District
class Office(models.Model):
    name = models.CharField(max_length=150)  # can be officename
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="offices")
    officetype = models.CharField(max_length=50, blank=True)
    pincode = models.CharField(max_length=10, blank=True)

    class Meta:
        unique_together = ("name", "district")  # Avoid duplicate office names per district

    def __str__(self):
        return f"{self.name} ({self.pincode})"