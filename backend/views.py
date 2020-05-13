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

        return render(request, 'heatMapByState.html', {'data':stateCount})
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
            "env":a,

        })