from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models


class NameMixin(models.Model):
    name = models.CharField(max_length=80, validators=[MinLengthValidator(5)], unique=True)

    class Meta:
        abstract = True


class ModifiedAtMixin(models.Model):
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class WinsMixin(models.Model):
    wins = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True