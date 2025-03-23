from django.db import models
from django.db.models.aggregates import Count


class AuthorManager(models.Manager):
    def get_authors_by_article_count(self):
        return self.annotate(article_count=Count('articles_authors')).order_by('-article_count', 'email')