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
    if len(lookupRes) == 0:
        return

    WEIGHT_LIMIT = 1800
    shippedRecord = {
        #'order_id': payload.data['order_id'], #model-> Order.objects()
        'shipped': []
    }

    #Second approach
    latestWeight = 0
    lookupResCopy = list(lookupRes)
    print('-----------LISTED lookupRes----------- NEW START', lookupRes)
    for i in lookupRes:
        packageWeightNow = 0
        for j in range(1, i['quantity']+1):
            jseen = j
            print('\n\n')
            print('1.i seen', i)
            print('2.j seen', j)
            if latestWeight <= WEIGHT_LIMIT and packageWeightNow <= WEIGHT_LIMIT:
                packageWeightNow = i['mass_g']
                latestWeight += packageWeightNow
                print('3.packageWeightNow in IF', packageWeightNow)
                print('4.latestWeight in IF', latestWeight, '\n\n\n')
            else:
                packageWeightNow -= i['mass_g']
                latestWeight -= i['mass_g']
                print('\n\n\n5.recursive breakpoint  in ELSE--')
                print('6.i seen in ELSE--', i)
                print('7.j seen in ELSE-- error at product number', jseen-1)
                #note that you need to slice all the remaining values
                partFulfilled = dict(i)
                partFulfilled['quantity'] -= (jseen-2) #might break for qty < 2?, check
                partRecord = {
                    'item_rem_count': jseen-2,
                    'item': partFulfilled
                }
                #print('packageWeightNow Trimmed in ELSE', packageWeightNow)
                #print('latestWeight Trimmed in ELSE', latestWeight)
                print('8.partRecord recursive breakpoint-- in ELSE', partRecord)
                print('9.partRecord-item-num in ELSE', partRecord['item']['quantity'])
                print('10.checking i[quantity] in  in ELSE', i['quantity'])

                if partRecord['item']['quantity'] != i['quantity']:
                    print('11.before partrecord', i)
                    print('\n\n12.partRecord going for recursion-- in ELSE', partRecord)
                    print('13.recursive compute call until the weight comes under 1.8kg and then print it out\n\n\n') 
                    
                    print('\n\n\n\n\n14a. CHECK lookupResCopy', lookupResCopy)
                    print('14b.CHECK partRecord', partRecord['item'])
                    #lookupResCopy[partRecord['item']['product_id']]['quantity'] =  partRecord['item']['quantity']
                    for num in range(len((lookupResCopy))):
                        if lookupResCopy[num]['product_id'] == partRecord['item']['product_id']:
                            lookupResCopy[num]['quantity'] = partRecord['item']['quantity']          

                    print('\n14c.updated lookupResCopy in ELSE', lookupResCopy)
                    print('15.partRecord VERIFICATION in ELSE', partRecord)
                    print('16.shippedRecord VERIFICATION before adding partRecord in ELSE', shippedRecord)

                    #now add the partial transxn to the same record
                    #if partRecord['item']['quantity']:
                    #shippedRecord['shipped'].append({'product_id': i['product_id'], 'quantity': i['quantity'] - partFulfilled['quantity']})
                    print('VAL CHECKS')
                    print('17.i-checks', i)
                    print('18.i[quantity]', i['quantity'])
                    print('19.partRecord[item][quantity]', partRecord['item']['quantity'])

                    print('VAL CHECKS')
                    updatedList = list(shippedRecord['shipped'])
                    #infliction point here - to send completed numbers till now
                    updatedList.append({'product_id': i['product_id'], 'quantity': jseen-2})
                    # RECENT updatedList.append({'product_id': i['product_id'], 'quantity': i['quantity'] - partRecord['item']['quantity'] + 1})
                    print('\n\n\n20.CHECKING UPDATEdLIST to be put in shippedRecord[shipped]', updatedList)
                    shippedRecord['shipped'] = updatedList
                    #shippedRecord['shipped'].append({'product_id': i['product_id'], 'quantity': i['quantity'] - partFulfilled['quantity']})
                    print('21.CHECKING shippedRecord[shipped]', shippedRecord['shipped'])
                    print('22.CHECKING type shippedRecord[shipped]\n\n\n', type(shippedRecord['shipped']))
                    print('23.shippedRecord seen OFFICIAL--', shippedRecord)
                    ship_package(lookupResCopy)
                    #break
                    return
                    #recursive compute call until the weight comes under 1.8kg and then print it out
                    #break


        print('end of an object list')
        if latestWeight <= WEIGHT_LIMIT:
                print('24.WEIGHT_LIMIT----', WEIGHT_LIMIT, '\n')
                shippedRecord['shipped'].append({'product_id': i['product_id'], 'quantity': i['quantity']})
                #print('25.shippedRecord seen IN PROGRESS', shippedRecord)
                #pop the completed lookup entry
                for item in lookupRes:
                    if item['product_id'] == i['product_id']:
                        lookupResCopy.remove(item)
                        print('26.updated lookupRes with removed rquest data', lookupResCopy)

        if i == lookupRes[-1]:
            print('25.shippedRecord seen FINAL OFFICIAL', shippedRecord)
                

        else:
            print('27.Over weight package seen')



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
    #is this coreect????
    for i in request.data['requested']:
        for j in lookupRes:
            if i['product_id'] == j['product_id']:
                j['quantity'] = i['quantity']
    #print('new lookupRes', lookupRes)
    ####ADDING PRE_SHIP_PACKAGE LOGIC

    #1ship_package(request)
    ship_package(lookupRes)

    print('-----------')

    return Response({"products": []})