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

def ship_package2(partRecord):
    print('\n\n\nship_package2 input seen', partRecord, '\n\n\n')
    #print('partRecord[quantity] seen', partRecord['item']['quantity'])
    #for i in range(partRecord['item']['quantity']):
    #    print(i)



def ship_package(lookupRes): #change name?? check once
        # ACTUAL SHIP PACKAGE LOGIC (maybe recursive)
    WEIGHT_LIMIT = 1800
    shippedRecord = {
        #'order_id': payload.data['order_id'], #model-> Order.objects()
        'shipped': []
    }

    #Second approach
    latestWeight = 0
    lookupResCopy = list(lookupRes)
    for i in lookupRes:
        packageWeightNow = 0
        for j in range(1, i['quantity']+1):
            jseen = j
            print('\n\n')
            print('i seen', i)
            print('j seen', j)
            if latestWeight < WEIGHT_LIMIT and packageWeightNow < WEIGHT_LIMIT:
                packageWeightNow = i['mass_g']
                latestWeight += packageWeightNow
                print('packageWeightNow in IF', packageWeightNow)
                print('latestWeight in IF', latestWeight, '\n\n\n')
            else:
                packageWeightNow -= i['mass_g']
                latestWeight -= i['mass_g']
                print('\n\n\nrecursive breakpoint  in ELSE--')
                print('j seen in ELSE', jseen-1)
                #note that you need to slice all the remaining values
                partFulfilled = dict(i)
                partFulfilled['quantity'] -= (jseen-2)
                partRecord = {
                    'item_num': jseen-2,
                    'item': partFulfilled
                }
                print('packageWeightNow Trimmed in ELSE', packageWeightNow)
                print('latestWeight Trimmed in ELSE', latestWeight)
                print('partRecord recursive breakpoint-- in ELSE', partRecord)
                print('partRecord-item-num in ELSE', partRecord['item_num'])
                print('checking i[quantity] in  in ELSE', i['quantity'])

                if partRecord['item_num'] != i['quantity']:
                    print('\n\npartRecord going for recursion-- in ELSE', partRecord)
                    print('recursive compute call until the weight comes under 1.8kg and then print it out\n\n\n') 
                    
                    print('\n\n\n\n\nCHECK lookupResCopy', lookupResCopy)
                    print('CHECK partRecord', partRecord['item'])
                    #lookupResCopy[partRecord['item']['product_id']]['quantity'] =  partRecord['item']['quantity']
                    for i in range(len((lookupResCopy))):
                        if lookupResCopy[i]['product_id'] == partRecord['item']['product_id']:
                            lookupResCopy[i]['quantity'] = partRecord['item']['quantity']          
                        #for j in range(partRecord['item'])):
                            #print('i-', i)
                            #print('j-', j)
                            #if i['product_id'] == j['product_id']:
                            #    i['quantity'] = j['product_id']

                    #for i in lookupResCopy:
                    #    for j in partRecord['item']:
                    #        if int(i['product_id']) == int(j['product_id']):
                    #            i['quantity'] = j['quantity']

                    print('updated lookupResCopy in ELSE', lookupResCopy)
                    print('updated partRecord in ELSE', partRecord)
                    ship_package2(lookupResCopy)
                    return
                    #recursive compute call until the weight comes under 1.8kg and then print it out
                #break


        print('end of an object list')
        if latestWeight < WEIGHT_LIMIT:
                #latestWeightSeen = packageWeight
                print('WEIGHT_LIMIT----', WEIGHT_LIMIT, '\n')
                #print('packageWeight before logging to DB', packageWeight, '\n')
                shippedRecord['shipped'].append({'product_id': i['product_id'], 'quantity': i['quantity']})
                print('shippedRecord seen', shippedRecord)
                #pop the completed lookup entry
                for item in lookupRes:
                    if item['product_id'] == i['product_id']:
                        lookupResCopy.remove(item)
                        print('updated lookupRes with removed rquest data', lookupResCopy)
                

        else:
            print('Over weight package seen')



@api_view(['POST'])    
def process_order(request):
    # storing order-id in orders table
    query = request.data

    Order.objects.create(order_id=query['order_id'])
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
    for i in request.data['requested']:
        for j in lookupRes:
            if i['product_id'] == j['product_id']:
                j['quantity'] = i['quantity']
    print('new lookupRes', lookupRes)
    ####ADDING PRE_SHIP_PACKAGE LOGIC

    #1ship_package(request)
    ship_package(lookupRes)

    print('-----------')

    return Response({"products": []})