#from django.http import JsonResponse,HttpResponseServerError
from .handler import handle_file, update_file, merge_files
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pika
from django.conf import settings
import tasks
import selectors


# @api_view(http_method_names=['POST'])
# def receive_file(request):
#     try:
#         handle_file(request.FILES['file'])
#         response = {
#                 'status': 'saved'
#             }
#         return Response(response, status=201)
#     except Exception as e:
#         print(e)
#         return HttpResponseServerError()
    

@api_view(http_method_names=['POST'])
def create(request):
    response = handle_file()
    return Response({
        'status' : 'File created',
        'file_name' : response
    }, status=201)

@api_view(http_method_names=['POST'])
def update(request):
    file_name = request.data['file_name']
    video_data = request.data['blob']
    update_file(file_name, data=video_data)
    
    return Response({
        'status' : 'Updated',
    }, status=201)

@api_view(http_method_names=['POST'])
def close(request):
    file_name = request.data['file_name']
    merge_files(file_name)
    connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
    channel = connection.channel()
    channel.queue_declare(queue=settings.RABBITMQ_QUEUE_NAME)
    channel.basic_publish(
        exchange='',
        routing_key=settings.RABBITMQ_QUEUE_NAME,
        body=file_name,
            )
    connection.close()
    return Response({
        'status' : 'Merge successful'
    }, status=201
    )

# Create your views here.
