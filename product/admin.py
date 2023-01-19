from django.contrib import admin

from .models import Product, Order, Summary
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'mass_g')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id',)

class SummaryAdmin(admin.ModelAdmin):
    list_display = ('order_id',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Summary, SummaryAdmin)
