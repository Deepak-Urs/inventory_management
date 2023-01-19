from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Product, Order, Summary
from .serializers import ProductSerializer


# Create your views here.
class ProductsList(APIView):
    #
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

def ship_package(payload):
    print('payload received', payload.data)
    
    print('requestedItems received')
    #products = Product.objects.filter(product_id=payload.data['requested']).values()
    #payload.data['requested'].

    #list = []
    #for id in payload.data['requested']:
    #    list.append(Product.objects.filter(product_id=payload.data['requested'][id]).values())
    
    print(list)
    
    #serializer = ProductSerializer(products, many=True)
    #print('existing data --', serializer.data)
    
    #incoming response data above in Orderedict

@api_view(['POST'])    
def process_order(request):
    #Order.objects.create(order_id=query['order_id'])
    ship_package(request)

    print('-----------')

    return Response({"products": []})