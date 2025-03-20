from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.mixins import LastUpdatedMixin, IsAwardedMixin


# Create your models here.

class BasePerson(models.Model):
    full_name = models.CharField(max_length=120, validators=[MinLengthValidator(2), MaxLengthValidator(120)])
    birth_date = models.DateField(default='1900-01-01')
    nationality = models.CharField(max_length=50, default='Unknown', validators=[MaxLengthValidator(50)])

    class Meta:
        abstract = True

class Director(BasePerson):
    years_of_experience= models.SmallIntegerField(default=0, validators=[MinValueValidator(0)])

class Actor(BasePerson, LastUpdatedMixin, IsAwardedMixin):
   pass

class Movie(models.Model, LastUpdatedMixin, IsAwardedMixin):
    class MovieTypes(models.TextChoices):
        ACTION = 'Action', 'Action'
        COMEDY = 'Comedy', 'Comedy'
        DRAMA = 'Drama', 'Drama'
        OTHER = 'Other', 'Other'

    title = models.CharField(max_length=150, validators=[MinLengthValidator(5), MaxLengthValidator(150)])
    release_date = models.DateField()
    storyline = models.TextField(null=True, blank=True)
    genre= models.CharField(max_length=6, choices=MovieTypes,  default= 'Other')
    rating = models.DecimalField(decimal_places=1, max_digits=3, validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    is_classic = models.BooleanField(default=False)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    starring_actor = models.ForeignKey(Actor, on_delete=models.CASCADE, null=True)
    actors = models.ManyToManyField(Actor)