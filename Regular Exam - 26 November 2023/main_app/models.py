from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, URLValidator
from django.db import models

from main_app.managers import AuthorManager
from main_app.mixins import ContentMixin, PublishedOnMixin


# Create your models here.
class Author(models.Model):
    full_name=models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    email=models.EmailField(unique=True)
    is_banned=models.BooleanField(default=False)
    birth_year=models.PositiveIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2005)])
    website=models.URLField(null=True, blank=True)
    objects=AuthorManager()



class Article(ContentMixin, PublishedOnMixin, models.Model):
    CATEGORIES = [
        ('Technology', 'Technology'),
        ('Science', 'Science'),
        ('Education', 'Education')
    ]

    title=models.CharField(max_length=200, validators=[MinLengthValidator(5)])
    category=models.CharField(choices=CATEGORIES,max_length=10, default='Technology')
    authors=models.ManyToManyField(Author, related_name='articles_authors')

class Review(ContentMixin, PublishedOnMixin, models.Model):
    rating = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    author=models.ForeignKey(Author, on_delete=models.CASCADE, related_name='review_author')
    article=models.ForeignKey(Article, on_delete=models.CASCADE, related_name='review_article')


