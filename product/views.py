from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer


# Create your views here.
class ProductsList(APIView):
    def get(self, request, format=None):
        print("ProductsList being called!")
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
