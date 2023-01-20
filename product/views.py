from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Product, Order, Summary
from .serializers import ProductSerializer, SummarySerializer


postQueryResult =[]
class ProductsList(APIView):
    def get(self):

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


def ship_package(lookupRes):
    if len(lookupRes) == 0:
        return

    WEIGHT_LIMIT = 1800
    latestId = Order.objects.all().count()
    shippedRecord = {
        'order_id': Order.objects.values()[latestId-1]['order_id'],
        'shipped': []
    }

    latestWeight = 0
    lookupResCopy = list(lookupRes)

    for i in lookupRes:
        packageWeightNow = 0
        for j in range(1, i['quantity']+1):
            jseen = j
            if latestWeight <= WEIGHT_LIMIT and packageWeightNow <= WEIGHT_LIMIT:
                packageWeightNow = i['mass_g']
                latestWeight += packageWeightNow
            else:
                packageWeightNow -= i['mass_g']
                latestWeight -= i['mass_g']
                partFulfilled = dict(i)
                partFulfilled['quantity'] -= (jseen-2)
                partRecord = {
                    'item': partFulfilled
                }
                if partRecord['item']['quantity'] != i['quantity']:  
                    for num in range(len((lookupResCopy))):
                        if lookupResCopy[num]['product_id'] == partRecord['item']['product_id']:
                            lookupResCopy[num]['quantity'] = partRecord['item']['quantity']          
                    #now adding the partial transxn to the same record
                    updatedList = list(shippedRecord['shipped'])
                    updatedList.append({'product_id': i['product_id'], 'quantity': jseen-2})
            
                    shippedRecord['shipped'] = updatedList
                    print(shippedRecord)
                    postQueryResult.append(shippedRecord)

                    #Summary table push operation -
                    orderId = Order.objects.values()[latestId-1]['order_id']
                    #productId = Product.objects.get(product_id=i['product_id'])
                    for i in shippedRecord['shipped']:    
                        Summary.objects.create(order_id=orderId,product_id=i['product_id'],quantity=i['quantity'])

                    #update order with the lookupResCopy details
                    ship_package(lookupResCopy)
                    return

        if latestWeight <= WEIGHT_LIMIT:
                shippedRecord['shipped'].append({'product_id': i['product_id'], 'quantity': i['quantity']})

                #pop the completed lookup entry
                for item in lookupRes:
                    if item['product_id'] == i['product_id']:
                        lookupResCopy.remove(item)

        if i == lookupRes[-1]:
            print(shippedRecord)   
            postQueryResult.append(shippedRecord)    


@api_view(['POST'])    
def process_order(request):
    # storing order-id in orders table
    query = request.data

    # dynamic value of order_id as an extra option if needed
    # newId = Order.objects.all().count() +1
    # Order.objects.create(order_id=newId)

    #utilizing the payload order_id and just utilizing it directly
    Order.objects.create(order_id=query['order_id'])
    
    #### ADDING PRE_SHIP_PACKAGE LOGIC
    print('\npayload received', request.data)
    products = Product.objects.values()
    

    # Capturing the data of the input product ids
    pids = []
    for i in request.data['requested']:
        pids.append(i['product_id'])

    
    lookupRes = []
    for entry in products:
        if entry['product_id'] in pids:
            lookupRes.append(entry)

    # updating the quantities --   
    for i in request.data['requested']:
        for j in lookupRes:
            if i['product_id'] == j['product_id']:
                j['quantity'] = i['quantity']

    ####END OF PRE_SHIP_PACKAGE LOGIC

    # call API here
    ship_package(lookupRes)
    return Response(postQueryResult)


@api_view(['POST'])
def shipPackage(shipment):
    summary = Summary.objects.filter(order_id=shipment.data['shipment'])
    serializer = SummarySerializer(summary, many=True)

    resList = list(serializer.data)

    return Response(resList)