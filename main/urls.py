from django.urls import include, path
from .views import *

urlpatterns = [
    path('', index , name=''),
    path('result/<str:query>', result, name='result')
]