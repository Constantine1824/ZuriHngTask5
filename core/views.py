from django.shortcuts import render
from django.http import JsonResponse,HttpResponseServerError
from .handler import handle_file
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(http_method_names=['POST'])
def receive_file(request):
    try:
        handle_file(request.FILES['file'])
        response = {
                'status': 'saved'
            }
        return Response(response, status=201)
    except Exception as e:
        print(e)
        return HttpResponseServerError()
# Create your views here.
