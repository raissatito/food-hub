from django.urls import include, path
from .views import *

urlpatterns = [
    path('', index , name='index'),
    path('result/<str:query>', result, name='result'),
    path('analyze', analyze, name='analyze'),
    path('analyze-result/<str:payload>', analyze_result, name='analyze-result'),
    path('discover', discover, name='discover'),
    path('delete/<int:recipe_id>', delete, name='delete'),
    path('set-visibility/<int:recipe_id>', set_visibility, name='set-visibility')
]

