from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.managers import PublisherManager
from main_app.mixins import NameMixin, CountryMixin, RatingMixin, UpdatedAtMixin


# Create your models here.
class Publisher(NameMixin, CountryMixin, RatingMixin):
    established_date = models.DateField(default='1800-01-01')
    objects = PublisherManager()


class Author(NameMixin, CountryMixin, UpdatedAtMixin):
    birth_date=models.DateField(null=True, blank=True)
    is_active=models.BooleanField(default=True)

class GenreChoices(models.TextChoices):
    FICTION = 'Fiction', 'Fiction'
    NONFICTION = 'Non-Fiction', 'Non-Fiction'
    OTHER = 'Other', 'Other'

class Book(RatingMixin,UpdatedAtMixin):
    title=models.CharField(max_length=200, validators=[MinLengthValidator(2)])
    publication_date=models.DateField()
    summary=models.TextField(blank=True, null=True)
    genre=models.CharField(max_length=11, default=GenreChoices.OTHER, choices = GenreChoices)
    price =models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01), MaxValueValidator(9999.99)], default=0.01)
    is_bestseller=models.BooleanField(default=False)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='book_publisher')
    main_author=models.ForeignKey(Author, on_delete=models.CASCADE, related_name='main_author')
    co_authors= models.ManyToManyField(Author, related_name='co_authors')

