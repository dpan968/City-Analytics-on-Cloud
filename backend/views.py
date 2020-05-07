from django.http import JsonResponse
from django.shortcuts import render
import json
import couchdb2
def pong(request):
    if request.method == 'GET':
        print("receive request")
        server1 = couchdb2.Server('http://admin:1234@115.146.94.150:8000/')
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
                    data.append([row.key[1],row.value/(row.value+enCount)])
                else:
                    data.append([row.key[1], 1])


        return JsonResponse({

            "message":data
        })

def templateTest(request):
    if request.method == "GET":
        print("receive request")
        server1 = couchdb2.Server('http://admin:1234@115.146.94.150:8000/')
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
        print("123")
        return render(request,'test.html',{'data':list})

def language(request):
    if request.method == 'GET':
        print("receive request")
        server1 = couchdb2.Server('http://admin:1234@115.146.94.150:8000/')
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
        return render(request, 'language.html', {'data': data})