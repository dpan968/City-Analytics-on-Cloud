from django.http import JsonResponse
from django.shortcuts import render
import json
from .utils import StateLocation
import couchdb2
import os
import socket
ip = os.environ.get('DB')
address = "http://admin:1234@" + ip + ":5985/"


def pong(request):
    if request.method == "GET":
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


def heatByState(request):
    if request.method == "GET":
        stateCount = {
            'vic': 0,
            'nsw': 0,
            'sa': 0,
            'qsl': 0,
            'wa': 0,
            'tas': 0,
            'nt': 0,
            'act': 0
        }
        try:
            statLocation = StateLocation()
            server1 = couchdb2.Server(address)
            db = server1['tweets']
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
            for key in stateCount:
                stateCount[key] = stateCount[key]/1000
            cache = open('backend/cache/stateCountCache.json','w')
            json.dump(stateCount,cache)
            cache.close()
        except BaseException:
            print("error in connecting to the database")
            cache = open('backend/cache/stateCountCache.json','r')
            stateCount = json.load(cache)
            cache.close()
        finally:
            return render(request, 'heatMapByState.html', {'data':stateCount,'aurin':readPopulation()})

def heatMapOrigin(request):
    if request.method == "GET":
        list = []
        try:
            server1 = couchdb2.Server(address)
            db = server1['tweets']


            result = db.view('/abc', 'testView2', group=True, group_level=2, reduce=True)
            sum = 0
            for row in result:
                item = {
                    'location': row.key,
                    'count': row.value
                }
                sum += row.value
                list.append(item)
            cache = open('backend/cache/heatMapOrigin.json','w')
            json.dump(list,cache)
            cache.close()
        except BaseException:
            print("error in connecting to the database")
            cache = open('backend/cache/heatMapOrigin.json','r')
            list = json.load(cache)
            cache.close()
        finally:
            return render(request,'test.html',{'data':list})

def language(request):
    if request.method == 'GET':
        languageState = {}
        languageOrigin = []
        try:
            server1 = couchdb2.Server(address)
            db = server1['tweets']
            result = db.view('/abc', 'language', group=True, group_level=2, reduce=True)
            en = {}
            languageOrigin = []
            for row in result:
                if row.key[0] == "en":
                    en[tuple(row.key[1])] = row.value
                else:
                    if tuple(row.key[1]) in en:
                        enCount = en.get(tuple(row.key[1]))
                        item = {
                            'location':row.key[1],
                            'count':row.value/(row.value+enCount)
                        }
                        languageOrigin.append(item)
                    else:
                        item = {
                            'location':row.key[1],
                            'count':1
                        }
                        languageOrigin.append(item)
            for item in languageOrigin:
                item['count'] = round(item['count'],4)
            languageState = languageByState(result)

            cache1 = open('backend/cache/languageOrigin.json','w')
            json.dump(languageOrigin,cache1)
            cache1.close()
            cache2 = open('backend/cache/languageState.json','w')
            json.dump(languageState,cache2)
            cache2.close()
        except BaseException:
            print("error in connecting to the database")
            cache1 = open('backend/cache/languageOrigin.json','r')
            languageOrigin = json.load(cache1)
            cache1.close()
            cache2 = open('backend/cache/languageState.json','r')
            languageState = json.load(cache2)
            cache2.close()
        finally:
            return render(request, 'language.html', {'data': languageOrigin,"aurin":heatByStateAurin(),'rate':readLanguageByState(),'languageStateRate':languageState})
    
def index(request):
    if request.method == 'GET':
        return render(request, 'index.html', {})

def test(request):
    if request.method == 'GET':
        myname = socket.getfqdn(socket.gethostname())
        myaddr = socket.gethostbyname(myname)
        return JsonResponse({
            "name":myname,
            "ip":myaddr
        })
def languageByState(result):
    stateEnCount = {
        'vic': 0,
        'nsw': 0,
        'sa': 0,
        'qsl': 0,
        'wa': 0,
        'tas': 0,
        'nt': 0,
        'act': 0
    }

    stateTotalCount = {
        'vic': 0,
        'nsw': 0,
        'sa': 0,
        'qsl': 0,
        'wa': 0,
        'tas': 0,
        'nt': 0,
        'act': 0
    }
    statLocation = StateLocation()
    stateCount = {}
    for row in result:
        location = row.key[1]
        if row.key[0] != "en":
            if statLocation.inVIC(location):
                stateEnCount['vic'] += row.value
            elif statLocation.inNSW(location):
                stateEnCount['nsw'] += row.value
            elif statLocation.inSA(location):
                stateEnCount['sa'] += row.value
            elif statLocation.inQSL(location):
                stateEnCount['qsl'] += row.value
            elif statLocation.inWA(location):
                stateEnCount['wa'] += row.value
            elif statLocation.inTas(location):
                stateEnCount['tas'] += row.value
            elif statLocation.inNT(location):
                stateEnCount['nt'] += row.value
            elif statLocation.inCT(location):
                stateEnCount['ct'] += row.value
        if statLocation.inVIC(location):
            stateTotalCount['vic'] += row.value
        elif statLocation.inNSW(location):
            stateTotalCount['nsw'] += row.value
        elif statLocation.inSA(location):
            stateTotalCount['sa'] += row.value
        elif statLocation.inQSL(location):
            stateTotalCount['qsl'] += row.value
        elif statLocation.inWA(location):
            stateTotalCount['wa'] += row.value
        elif statLocation.inTas(location):
            stateTotalCount['tas'] += row.value
        elif statLocation.inNT(location):
            stateTotalCount['nt'] += row.value
        elif statLocation.inCT(location):
            stateTotalCount['ct'] += row.value

    for state in stateTotalCount:
        if stateTotalCount[state] == 0:
            stateCount[state] = 0
        else:
            stateCount[state] = round(stateEnCount[state]/stateTotalCount[state],4)
    return stateCount


def dayAndTime(request):
    if request.method == 'GET':
        day = []
        time = []
        try:
            server1 = couchdb2.Server(address)
            db = server1['tweets']
            result = db.view('/abc', 'day', group=True, group_level=1, reduce=True)

            for row in result:
                item = {
                    'day': row.key,
                    'frequency': row.value
                }
                day.append(item)

            result = db.view('/abc', 'time', group=True, group_level=1, reduce=True)

            for row in result:
                item = {
                    'time': row.key,
                    'frequency': row.value
                }
                time.append(item)
            cache1 = open('backend/cache/day.json', 'w')
            json.dump(day, cache1)
            cache1.close()

            cache2 = open('backend/cache/time.json', 'w')
            json.dump(time, cache2)
            cache2.close()
        except BaseException:
            print("error in connecting to database")
            cache1 = open('backend/cache/day.json', 'r')
            day = json.load(cache1)
            cache1.close()

            cache2 = open('backend/cache/time.json', 'r')
            time = json.load(cache2)
            cache2.close()
        finally:
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

    for key in statePopulation:
        statePopulation[key]  = statePopulation[key]/1000
    return statePopulation




def readLanguageByState():
    stateTotal = {
        'vic': 0,
        'nsw': 0,
        'sa': 0,
        'qsl': 0,
        'wa': 0,
        'tas': 0,
        'nt': 0,
        'act': 0
    }
    stateEngElse = {
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
        '1': 'nsw',
        '2': 'vic',
        '3': 'qsl',
        '4': 'sa',
        '5': 'wa',
        '6': 'tas',
        '7': 'nt',
        '8': 'act'
    }
    file = open("backend/languageByState.json")
    data = ""
    while True:
        line = file.readline()
        if not line:
            break
        data += line

    originalJson = json.loads(data)
    for i in originalJson["features"]:
        properties = i["properties"]
        total = properties["person_tot_tot"]-properties["person_lang_spkn_home_notstated_tot"]
        engElse = properties["person_spks_oth_lang_tot"]
        stateId = properties["gcc_code16"][0]
        if stateId in stateDict:
            state = stateDict[stateId]
            stateTotal[state] += total
            stateEngElse[state] += engElse
    stateEngElseRate = dict()
    for i in stateTotal:
        stateEngElseRate[i] = round(stateEngElse[i]/stateTotal[i],4)
    return stateEngElseRate


def heatByStateAurin():
    file = open("backend/aurin.geojson")
    data = ""
    while True:
        line = file.readline()
        if not line:
            break
        data += line
    aurin = json.loads(data)
    return aurin