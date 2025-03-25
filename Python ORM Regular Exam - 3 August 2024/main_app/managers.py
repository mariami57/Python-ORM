from django.db import models


class AstronautManager(models.Manager):
    def get_astronauts_by_missions_count(self):
        return (self.annotate(num_missions=models.Count('passengers'))
                .order_by('-num_missions', 'phone_number'))