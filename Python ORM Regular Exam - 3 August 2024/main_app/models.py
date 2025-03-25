from django.core.validators import MinLengthValidator, MinValueValidator, RegexValidator
from django.db import models

from main_app.managers import AstronautManager
from main_app.mixins import UpdatedAtMixin, NameMixin, LaunchDateMixin
from main_app.validators import DigitsOnlyValidator


# Create your models here.
class Astronaut(NameMixin, UpdatedAtMixin):
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\d{1,15}$')],
        unique=True)

    is_active = models.BooleanField(default=True)

    date_of_birth = models.DateField(blank=True, null=True)

    spacewalks = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    objects = AstronautManager()


class Spacecraft(NameMixin, UpdatedAtMixin, LaunchDateMixin):
    manufacturer = models.CharField(max_length=100)
    capacity = models.SmallIntegerField(validators=[MinValueValidator(1)])
    weight = models.FloatField(validators=[MinValueValidator(0.0)])


class Status(models.TextChoices):
    PLANNED = 'Planned', 'Planned'
    ONGOING = 'Ongoing', 'Ongoing'
    COMPLETED = 'Completed', 'Completed'

class Mission(NameMixin, UpdatedAtMixin, LaunchDateMixin):
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=9, choices=Status, default=Status.PLANNED.value)
    spacecraft = models.ForeignKey(Spacecraft, on_delete=models.CASCADE, related_name='used_in_missions')
    astronauts = models.ManyToManyField(Astronaut, related_name='passengers')
    commander = models.ForeignKey(Astronaut, on_delete=models.SET_NULL, null=True, related_name='commanded_missions')
