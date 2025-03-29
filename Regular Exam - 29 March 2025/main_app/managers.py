from django.db import models


class PublisherManager(models.Manager):
    def get_publishers_by_books_count(self):
        return (self.annotate(books_count=models.Count('book_publisher'))
                .order_by('-books_count', 'name'))