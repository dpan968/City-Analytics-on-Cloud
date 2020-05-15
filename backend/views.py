from django.http import JsonResponse
from django.shortcuts import render
import json
from .utils import StateLocation
import couchdb2
import os

ip = os.environ.get('DB')
address = "http://admin:1234@" + ip + ":5984/"
a = os.environ.get('TEST')
file = open("backend/aurin.geojson")
data = ""
while True:
    line = file.readline()
    if not line:
        break
    data += line
aurin = json.loads(data)
def pong(request):
    if request.method == "GET":
        print("address")

        server1 = couchdb2.Server(address)
        db = server1['tweets']

        list = []
        result = db.view('/abc', 'testView2', group=True, group_level=2, reduce=True)
        sum = 0
        for row in result:
            item = {
                'location': row.key,
                'count': row.value
            }
            sum += row.value
            list.append(item)

        return JsonResponse({

            "message":list
        })


# def test(request):
#     if request.method == "GET":
#         statLocation = StateLocation()
#         print("receive request")
#         server1 = couchdb2.Server('http://admin:1234@115.146.94.150:8000/')
#         db = server1['tweets']
#
#         list = []
#         result = db.view('/abc', 'testView2', group=True, group_level=2, reduce=True)
#         for row in result:
#             item = {
#                 'location': row.key,
#                 'count': row.value
#             }
#             if statLocation.inCT(item['location']):
#                 list.append(item)
#
#         return render(request,'heatMapByState.html',{'data':list})


def heatByState(request):
    if request.method == "GET":
        statLocation = StateLocation()
        print("receive request")
        server1 = couchdb2.Server(address)
        db = server1['tweets']

        stateCount = {
            'vic' : 0,
            'nsw' : 0,
            'sa' : 0,
            'qsl' : 0,
            'wa' : 0,
            'tas' : 0,
            'nt' : 0,
            'act' : 0
        }


        result = db.view('/abc', 'testView2', group=True, group_level=2, reduce=True)
        for row in result:
            item = {
                'location': row.key,
                'count': row.value
            }
            if statLocation.inVIC(item['location']):
                stateCount['vic'] += item['count']
            elif statLocation.inNSW(item['location']):
                stateCount['nsw'] += item['count']
            elif statLocation.inSA(item['location']):
                stateCount['sa'] += item['count']
            elif statLocation.inQSL(item['location']):
                stateCount['qsl'] += item['count']
            elif statLocation.inWA(item['location']):
                stateCount['wa'] += item['count']
            elif statLocation.inTas(item['location']):
                stateCount['tas'] += item['count']
            elif statLocation.inNT(item['location']):
                stateCount['nt'] += item['count']
            elif statLocation.inCT(item['location']):
                stateCount['ct'] += item['count']

        return render(request, 'heatMapByState.html', {'data':stateCount,'aurin':readPopulation()})
        # return JsonResponse({
        #     'data': stateCount
        # })




def heatMapOrigin(request):
    if request.method == "GET":
        print("receive request")
        server1 = couchdb2.Server(address)
        db = server1['tweets']

        list = []
        result = db.view('/abc', 'testView2', group=True, group_level=2, reduce=True)
        sum = 0
        for row in result:
            item = {
                'location': row.key,
                'count': row.value
            }
            sum += row.value
            list.append(item)

        return render(request,'test.html',{'data':list})

def language(request):
    if request.method == 'GET':
        print("receive request")
        server1 = couchdb2.Server(address)
        db = server1['tweets']

        list = []
        result = db.view('/abc', 'language', group=True, group_level=2, reduce=True)
        en = {}
        ot = {}
        data = []
        for row in result:
            # item = {
            #     'location': row.key,
            #     'count': row.value
            # }
            if row.key[0] == "en":
                a = tuple(row.key[1])
                en[tuple(row.key[1])] = row.value
            else:
                if tuple(row.key[1]) in en:
                    enCount = en.get(tuple(row.key[1]))
                    item = {
                        'location':row.key[1],
                        'count':row.value/(row.value+enCount)
                    }
                    data.append(item)
                else:
                    item = {
                        'location':row.key[1],
                        'count':1
                    }
                    data.append(item)
        return render(request, 'language.html', {'data': data,"aurin":aurin})
    
def index(request):
    if request.method == 'GET':
        return render(request, 'index.html', {})

def test(request):
    if request.method == 'GET':

        return JsonResponse({
            "aurin":readPopulation(),
        })

def dayAndTime(request):
    if request.method == 'GET':
        server1 = couchdb2.Server(address)
        db = server1['tweets']

        list = []
        result = db.view('/abc', 'day', group=True, group_level=1, reduce=True)
        day = []
        for row in result:
            item = {
                'day': row.key,
                'frequency': row.value
            }
            day.append(item)

        result = db.view('/abc', 'time', group=True, group_level=1, reduce=True)
        time = []
        for row in result:
            item = {
                'time': row.key,
                'frequency': row.value
            }
            time.append(item)
        #return JsonResponse({'day':day,'time':time})
        return render(request, 'daytime.html', {'day':day,'time':time})


def readPopulation():
    statePopulation = {
        'vic': 0,
        'nsw': 0,
        'sa': 0,
        'qsl': 0,
        'wa': 0,
        'tas': 0,
        'nt': 0,
        'act': 0
    }
    stateDict = {
        '1 ': 'nsw',
        '2 ': 'vic',
        '3 ': 'qsl',
        '4 ': 'sa',
        '5 ': 'wa',
        '6 ': 'tas',
        '7 ': 'nt',
        '8 ': 'act'
    }
    file = open("backend/aurinPopulation.json")
    data = ""
    while True:
        line = file.readline()
        if not line:
            break
        data += line

    originalJson = json.loads(data)
    for i in originalJson["features"]:
        properties = i["properties"]
        areaPopulation = properties["persons_total"]
        state = stateDict[properties["state_code"]]
        statePopulation[state] += areaPopulation

    return statePopulation