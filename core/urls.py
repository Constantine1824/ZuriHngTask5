from django.urls import path
from .views import create,update

urlpatterns = [
    # path('upload', receive_file, name='upload'),
    path('create', create, name='Create-file'),
    path('update', update, name='update-file')
]
