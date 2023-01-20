from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Product, Order, Summary
from .serializers import ProductSerializer


# Create your views here.
class ProductsList(APIView):
    #
    def get(self, request, format=None):

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



def ship_package(lookupRes): #change name?? check once
        # ACTUAL SHIP PACKAGE LOGIC (maybe recursive)
    if len(lookupRes) == 0:
        return

    WEIGHT_LIMIT = 1800
    latestId = Order.objects.all().count()
    shippedRecord = {
        'order_id': Order.objects.values()[latestId-1]['order_id'], #model-> Order.objects()
        'shipped': []
    }

    print('Order.objects.values()[0:1]', Order.objects.values()[0]['order_id'])
    #Second approach
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
                #note that you need to slice all the remaining values
                partFulfilled = dict(i)
                partFulfilled['quantity'] -= (jseen-2) #might break for qty < 2?, check
                partRecord = {
                    'item_rem_count': jseen-2,
                    'item': partFulfilled
                }
                if partRecord['item']['quantity'] != i['quantity']:  
                    #lookupResCopy[partRecord['item']['product_id']]['quantity'] =  partRecord['item']['quantity']
                    for num in range(len((lookupResCopy))):
                        if lookupResCopy[num]['product_id'] == partRecord['item']['product_id']:
                            lookupResCopy[num]['quantity'] = partRecord['item']['quantity']          
                    #now add the partial transxn to the same record
                    #if partRecord['item']['quantity']:
                    #shippedRecord['shipped'].append({'product_id': i['product_id'], 'quantity': i['quantity'] - partFulfilled['quantity']})
                    updatedList = list(shippedRecord['shipped'])
                    #infliction point here - to send completed numbers till now
                    updatedList.append({'product_id': i['product_id'], 'quantity': jseen-2})
                    # RECENT updatedList.append({'product_id': i['product_id'], 'quantity': i['quantity'] - partRecord['item']['quantity'] + 1})
            
                    shippedRecord['shipped'] = updatedList
                    #shippedRecord['shipped'].append({'product_id': i['product_id'], 'quantity': i['quantity'] - partFulfilled['quantity']})
            
            
                    print('23.shippedRecord seen OFFICIAL--', shippedRecord)
                    #setup Summary table push operation -
                    orderId = Order.objects.values()[latestId-1]['order_id']
                    for i in shippedRecord['shipped']:    
                        #Summary.objects.create(
                        #    order_id = Order.objects.filter(order_id=i['order_id']),
                        #    product_id= Product.objects.filter(product_id=i['product_id']),
                        #    qty = i['quantity']
                        #)
                        Summary.objects.create(order_id=orderId,product_id=i['product_id'],quantity=i['quantity'])
                    ship_package(lookupResCopy)
                    #break
                    return
                    #recursive compute call until the weight comes under 1.8kg and then print it out
                    #break



        if latestWeight <= WEIGHT_LIMIT:

                shippedRecord['shipped'].append({'product_id': i['product_id'], 'quantity': i['quantity']})

                #pop the completed lookup entry
                for item in lookupRes:
                    if item['product_id'] == i['product_id']:
                        lookupResCopy.remove(item)


        if i == lookupRes[-1]:
            print('25.shippedRecord seen FINAL OFFICIAL', shippedRecord)
                

        #else:
        #    print('27.Over weight package seen')



@api_view(['POST'])    
def process_order(request):
    # storing order-id in orders table
    #query = request.data

    newId = Order.objects.all().count() +1
    Order.objects.create(order_id=newId)
    

    #make the above id as a auto incrwmnet value
    
    ####ADDING PRE_SHIP_PACKAGE LOGIC
    print('\npayload received', request.data)
    #products = list(Product.objects.filter(__in="")values()) --> SQL way
    products = Product.objects.values()
    

    # Capturing the data of the input param ids
    #pids = [i['product_id'] for i in payload.data['requested']] --> optimizastion pyhton coll?
    pids = []
    for i in request.data['requested']:
        pids.append(i['product_id'])

    
    lookupRes = []
    for entry in products:
        if entry['product_id'] in pids:
            lookupRes.append(entry)
    #overall alternative at 34 --> products = list(Product.objects.filter(__in=(pids))values())



    # calculating the weights --   
    newRec = []

    # orderRequest
    #is this coreect????
    for i in request.data['requested']:
        for j in lookupRes:
            if i['product_id'] == j['product_id']:
                j['quantity'] = i['quantity']

    ####ADDING PRE_SHIP_PACKAGE LOGIC

    #1ship_package(request)
    ship_package(lookupRes)

    print('-----------')

    return Response({"products": []})