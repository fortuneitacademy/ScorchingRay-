
from django.urls import path

from . import views

urlpatterns = [
    path('acme-challenge/',views.detail,name='detail'),
]