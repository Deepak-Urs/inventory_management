from rest_framework import serializers
from .models import Product, Order, Summary

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "mass_g",
            "product_name",
            "product_id"
        )

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = (
            "order_id",
        )

class SummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = Summary
        fields = (
            "order_id",
            "product_id",
            "qunatity"
        )