from django.urls import path
from .views import Home,upload,convert,ajax
from .forms import UploadFileForm


urlpatterns = [
    path('',Home.as_view(), name='home'),
    path('upload/',upload, name='upload'),
    path('convert/',convert, name='convert'),
    path('ajax/',ajax, name='ajax'),
]