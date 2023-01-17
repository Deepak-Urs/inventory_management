from django.db import models

# Create your models here.
class Product(models.Model):
    mass_g = models.IntegerField()
    product_name = models.CharField(max_length=255)
    product_id = models.IntegerField()

    class Meta:
        ordering = ('product_id',)

    def __str__(self):
        return self.product_name

