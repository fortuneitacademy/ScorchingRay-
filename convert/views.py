from unicodedata import name
from django.shortcuts import render
# Create your views here.
from django.views.generic import TemplateView,ListView
import urllib3
from .forms import UploadFileForm
from .stl_tools import numpy2stl
from scipy.ndimage import gaussian_filter
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import os
from django.core.files.storage import FileSystemStorage
from .models import Student
from matplotlib.pylab import imread, imshow
import pyrebase
import urllib
URL_IMG = ''
config = {
"apiKey": "AIzaSyAGz0NylOh-nKxBstZSN9wjHtql331Uxas",
"authDomain": "stlconverter-1f730.firebaseapp.com",
"projectId": "stlconverter-1f730",
"databaseURL": "https://stlconverter-1f730-default-rtdb.firebaseio.com",
"storageBucket": "stlconverter-1f730.appspot.com",
"messagingSenderId": "214485460624",
"appId": "1:214485460624:web:32025468feb52158321a15",
"measurementId": "G-QCZ2DSH4EG"
}


def convert(request):
    try:
        if request.method == 'POST':
            scale = float(request.POST['scale'])
            sigma = float(request.POST['sigma'])
            mask_val = float(request.POST["mask_val"])
            list_val = []
            ayth_storage = pyrebase.initialize_app(config)
            st = ayth_storage.storage()
            model = Student.objects.all()
            for mod in model:
                list_val.append({'img':mod.url_img,'stl':mod.img_name})
            scale = float(scale / 100)
            sigma = float(sigma / 10)
            mask_val = float(mask_val / 10)
            from imageio import imread
            A = imread(str(list_val[-1]['img']))  # read from rendered png
            A = A.mean(axis=2)  # grayscale projection
            A = gaussian_filter(A,sigma=sigma)  # smoothing
            stl_path = str(str(list_val[-1]['stl']))
            stl_path = stl_path.replace('.jpg','.stl')
            stl_path = stl_path.replace('.png','.stl')
            stl_path = stl_path.replace('.jpeg','.stl')
            numpy2stl(A, stl_path, scale=scale, mask_val=mask_val)
            return render(request,'home.html',{'img':str(list_val[-1]['img']),"stl":str(st.child(stl_path).get_url(None))})
        else:
            return HttpResponse(request,"val")
    except Exception as e:
        return HttpResponse(request,str(e))

    


def upload(request):
    if request.method == 'POST':
        ayth_storage = pyrebase.initialize_app(config)
        file2 = request.FILES["document"]
        st = ayth_storage.storage()
        cludname = 'photo/' + str(file2)
        st.child(cludname).put(file2)
        URL_IMG = str(st.child(cludname).get_url(None))
        model = Student.objects.create(url_img=URL_IMG,img_name=cludname)
        model.save()
        return render(request,'home.html',{'img_obj':str(st.child(cludname).get_url(None))})
    else:
        form = UploadFileForm()
    return render(request,'home.html',{'form':form})
    


class Home(TemplateView):
    template_name = 'home.html'