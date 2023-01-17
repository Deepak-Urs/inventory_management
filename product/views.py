from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Product
from .serializers import ProductSerializer


# Create your views here.
class ProductsList(APIView):
    def get(self, request, format=None):
        print("ProductsList being called!")
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    #def process_order(request, order_id, requested):
    #    print('process_order is called with --', request)
    #    print('process_order is called withorder_id --', order_id)
    #    print('process_order is called with requested--', requested)

    #    return Response({"products": []})

class ProcessOrder(APIView):
    def post(request):
        print('process_order is called with --', request)

        return Response({"products": []})

#def ship_package(payload):
#    pa

@api_view(['POST'])    
def process_order(request):
    print('process_order is called with --', request)
    query = request.data
    print('query seen', query)

    print('-----------')

    return Response({"products": []})