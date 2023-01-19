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
    print('\npayload received', payload.data)
    #products = list(Product.objects.filter(__in="")values()) --> SQL way
    products = Product.objects.values()
    

    # Capturing the data of the input param ids
    #pids = [i['product_id'] for i in payload.data['requested']] --> optimizastion pyhton coll?
    pids = []
    for i in payload.data['requested']:
        pids.append(i['product_id'])
    print('pids-', pids, '\n')
    
    lookupRes = []
    for entry in products:
        if entry['product_id'] in pids:
            lookupRes.append(entry)
    #overall alternative at 34 --> products = list(Product.objects.filter(__in=(pids))values())

    #print('\n lookupRes', lookupRes, '\n')

    # calculating the weights --   
    newRec = []

    # orderRequest
    for i in payload.data['requested']:
        for j in lookupRes:
            if i['product_id'] == j['product_id']:
                j['quantity'] = i['quantity']
    print('new lookupRes', lookupRes)

    # ACTUAL SHIP PACKAGE LOGIC (maybe recursive)
    WEIGHT_LIMIT = 1800
    shippedRecord = {
        'order_id': payload.data['order_id'], #model-> Order.objects()
        'shipped': []
    }


    #First approach
    #latestWeight = 0
    #for i in lookupRes:
    #    packageWeight = i['mass_g'] * i['quantity']
    #    latestWeight += packageWeight
    #    print('latestWeight before loop', latestWeight, '\n')
    #    if packageWeight < WEIGHT_LIMIT and latestWeight < WEIGHT_LIMIT:
    #        #latestWeightSeen = packageWeight
    #        print('WEIGHT_LIMIT----', WEIGHT_LIMIT, '\n')
    #        print('packageWeight', packageWeight, '\n')
    #        shippedRecord['shipped'].append({'product_id': i['product_id'], 'quantity': i['quantity']})
                 
    #        print('latestWeight', latestWeight, '\n')
    #    else:
    #        print('Over weight package seen')
    #        #recursive compute call until the weight comes under 1.8kg and then print it out
    #print('shippedRecord', shippedRecord)

    #Second approach
    latestWeight = 0
    for i in lookupRes:
        packageWeightNow = 0
        for j in range(i['quantity']):
            jseen = j + 1
            print('\n\n')
            print('i seen', i)
            print('j seen', jseen)
            if latestWeight < WEIGHT_LIMIT and packageWeightNow < WEIGHT_LIMIT:
                packageWeightNow = i['mass_g']
                latestWeight += packageWeightNow
                print('packageWeightNow in IF', packageWeightNow, '\n')
                print('latestWeight in IF', latestWeight, '\n')
            else:
                packageWeightNow -= i['mass_g']
                latestWeight -= i['mass_g']
                print('recursive breakpoint--')
                print('j seen', jseen-1)
                partFulfilled = i
                partFulfilled['quantity'] -= (jseen-2)
                partRecord = {
                    'item_num': jseen-2,
                    'item': partFulfilled
                }
                print('packageWeightNow in ELSE', packageWeightNow, '\n')
                print('latestWeight in ELSE', latestWeight, '\n')
                print('recursive breakpoint-- in ELSE', partRecord)
                #recursive compute call until the weight comes under 1.8kg and then print it out
                #break
                return
                #return recursionCall()


        print('end of an object list')
        if latestWeight < WEIGHT_LIMIT:
                #latestWeightSeen = packageWeight
                print('WEIGHT_LIMIT----', WEIGHT_LIMIT, '\n')
                #print('packageWeight before logging to DB', packageWeight, '\n')
                shippedRecord['shipped'].append({'product_id': i['product_id'], 'quantity': i['quantity']})
                print('shippedRecord seen', shippedRecord)
        else:
            print('Over weight package seen')



@api_view(['POST'])    
def process_order(request):
    # storing order-id in orders table
    query = request.data

    Order.objects.create(order_id=query['order_id'])
    #make the above id as a auto incrwmnet value
    ship_package(request)

    print('-----------')

    return Response({"products": []})