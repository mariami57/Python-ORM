from datetime import date

from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models

from main_app.managers import HouseManager
from main_app.mixins import NameMixin, ModifiedAtMixin, WinsMixin


# Create your models here.
class House(NameMixin, ModifiedAtMixin, WinsMixin):
    motto = models.TextField(blank=True, null=True)
    is_ruling = models.BooleanField(default=False)
    castle = models.CharField(blank=True, null=True, max_length=80)
    objects = HouseManager()


class BreathTypes(models.TextChoices):
     FIRE = 'Fire', 'Fire'
     ICE = 'Ice', 'Ice'
     LIGHTNING = 'Lightning', 'Lightning'
     UNKNOWN = 'Unknown', 'Unknown'

class Dragon(NameMixin, ModifiedAtMixin, WinsMixin):
    power = models.DecimalField(decimal_places=1, max_digits=3, default=1.0, validators=[MinValueValidator(1.0), MaxValueValidator(10.0)])
    breath = models.CharField(max_length=9, choices=BreathTypes.choices, default=BreathTypes.UNKNOWN)
    is_healthy = models.BooleanField(default=True)
    birth_date = models.DateField(default=date.today)
    house = models.ForeignKey(House,related_name='dragons', on_delete=models.CASCADE)

class Quest(NameMixin, ModifiedAtMixin):
    code=models.CharField(validators=[RegexValidator(regex=r'^[a-zA-Z#]{4}$')], unique=True, max_length=4)
    reward = models.FloatField(default=100.0)
    start_time = models.DateTimeField()
    dragons = models.ManyToManyField(Dragon, related_name='quests')
    host = models.ForeignKey(House, on_delete=models.CASCADE, related_name='quests')