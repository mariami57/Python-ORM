from tkinter.constants import CASCADE

from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import SET_NULL

from main_app.managers import TennisPlayerManager


# Create your models here.
class TennisPlayer(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(5)])
    birth_date = models.DateField()
    country = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)]
    )
    ranking = models.PositiveIntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(300)]
    )
    is_active = models.BooleanField(default=True)

    objects = TennisPlayerManager()

class SurfaceTypes(models.TextChoices):
    NOT_SELECTED = 'Not Selected', 'Not Selected'
    CLAY = 'Clay', 'Clay'
    GRASS = 'Grass', 'Grass'
    HARD_COURT = 'Hard Court', 'Hard Court'

class Tournament(models.Model):

    name = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(2)],
        unique=True
    )
    location = models.CharField(max_length=100,
    validators=[MinLengthValidator(2)],)

    prize_money = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    start_date = models.DateField()

    surface_type = models.CharField(
        choices=SurfaceTypes,
        max_length=12,
        default=SurfaceTypes.NOT_SELECTED,
    )



class Match(models.Model):

    class Meta:
        verbose_name_plural = 'Matches'

    score = models.CharField(max_length=100)
    summary = models.TextField(validators=[MinLengthValidator(5)])
    date_played = models.DateTimeField()
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='matches')
    players = models.ManyToManyField(TennisPlayer, related_name='matches')
    winner = models.ForeignKey(TennisPlayer, on_delete=SET_NULL, null=True, related_name='won_matches')

