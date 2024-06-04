from django.urls import path
from .views import *

urlpatterns = [
    path('', contrato_view, name='contrato'),    
    path('consulta/', consulta_view, name='consulta'),
]
