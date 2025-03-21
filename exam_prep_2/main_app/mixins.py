from django.db import models

class CreteDateMixin(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True