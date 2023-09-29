from django.shortcuts import render
from django.http import JsonResponse,HttpResponseServerError
from .handler import handle_file
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def receive_file(request):
    if request.method == 'POST':
        try:
            handle_file(request.FILES['file'])
            response = {
                'status': 'saved'
            }
            return JsonResponse(response)
        except Exception as e:
            print(e)
            return HttpResponseServerError()
# Create your views here.
