from django.db import models

# Create your models here.
class Product(models.Model):
    mass_g = models.IntegerField()
    product_name = models.CharField(max_length=255)
    product_id = models.IntegerField()
    #quantity = models.IntegerField(default=0)

    class Meta:
        ordering = ('product_id',)

    def __str__(self):
        return self.product_name

class Order(models.Model):
    order_id = models.IntegerField()

    class Meta:
        ordering = ('order_id',)

class Summary(models.Model):
    order_id = models.ForeignKey(Order, related_name='Order', on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, related_name='Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        ordering = ('order_id',)

