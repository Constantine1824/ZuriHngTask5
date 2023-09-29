from django.urls import path
from .views import receive_file

urlpatterns = [
    path('upload', receive_file, name='upload')
]
