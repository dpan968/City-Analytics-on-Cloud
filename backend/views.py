from django.http import JsonResponse
import couchdb2
def pong(request):
    if request.method == 'GET':
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
        return JsonResponse({

            "message":list
        })