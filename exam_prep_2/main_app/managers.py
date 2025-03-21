from django.db import models


class ProfileManager(models.Manager):
    def get_regular_customers(self):
        customer_orders= self.annotate(orders_count=models.Count('customer_orders'))
        return customer_orders.filter(orders_count__gt=2).order_by('-orders_count')