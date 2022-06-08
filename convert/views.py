from unicodedata import name
from django.shortcuts import render
# Create your views here.
from django.views.generic import TemplateView,ListView
import urllib3
from .forms import UploadFileForm
from .stl_tools import numpy2stl
from scipy.ndimage import gaussian_filter
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse,Http404
from django.shortcuts import render
import os
from django.core.files.storage import FileSystemStorage
from .models import Student
from matplotlib.pylab import imread, imshow
import pyrebase,threading
import urllib
from django.template import loader
from environs import Env

URL_IMG = ''
env = Env()
env.read_env()


config = {
    "apiKey":env.str("apiKey"),
    "authDomain":env.str("authDomain"),
    "projectId":env.str("projectId"),
    "databaseURL":env.str("databaseURL"),
    "storageBucket":env.str("storageBucket"),
    "messagingSenderId":env.str("messagingSenderId"),
    "appId":env.str("appId"),
    "measurementId":env.str("measurementId"),
}


def convert(request):
    try:
        global finish
        if request.method == 'POST':
            scale = float(request.POST['scale'])
            sigma = float(request.POST['sigma'])
            mask_val = float(request.POST["mask_val"])
            list_val = []
            ayth_storage = pyrebase.initialize_app(config)
            st = ayth_storage.storage()
            model = Student.objects.all()
            for mod in model:
                if 3 < len(mod.url_img) and 3 <len(mod.img_name):
                    list_val.append({'img':mod.url_img,'stl':mod.img_name})
            scale = float(scale / 100)
            sigma = float(sigma / 10)
            mask_val = float(mask_val / 10)
            finish = False
            from imageio import imread
            A = imread(str(list_val[-1]['img']))  # read from rendered png
            A = A.mean(axis=2)  # grayscale projection
            A = gaussian_filter(A,sigma=sigma)  # smoothing
            stl_path = str(str(list_val[-1]['stl']))
            stl_path = stl_path.replace('.jpg','.stl')
            stl_path = stl_path.replace('.png','.stl')
            stl_path = stl_path.replace('.jpeg','.stl')
            def start_convert(A, stl_path, scale, mask_val):
                global finish
                lo = loader.get_template('home.html')
                lo.render()
                numpy2stl(A, stl_path, scale=scale, mask_val=mask_val)
                
            t = threading.Thread(target=start_convert,args=(A, stl_path, scale, mask_val))
            t.name = stl_path
            t.deamond = True
            t.start()
            Student.objects.all().delete()
            return render(request,'home.html',{'img':str(list_val[-1]['img']),'stl_org':str(stl_path),"stl":str(st.child(stl_path).get_url(None)),'finish':lambda:finish})
        else:
            return render(request,'home.html')
    except Exception as e:
        return render(request,'home.html')

    
def ajax(request):
    try:
        req = request.GET
        if req['request'] == 'stl':
            try:
                models = Student.objects.get(url_stl=str(req['value']))
                models.save()
                return JsonResponse({'wait':False})
            except:
                return JsonResponse({'wait':True})
        elif req['request'] == 'progress':
            status = []
            for thrd in threading.enumerate():
                if 'stl' in str(thrd.name):
                    status.append(thrd.name)
            if len(status) > 0:
                return JsonResponse({'status':True})
            else:
                return JsonResponse({'status':False})
        elif req['request'] == 'cancel':
            status = []
            for thrd in threading.enumerate():
                if 'stl' in str(thrd.name):
                    status.append(thrd.name)
            if len(status) == 0:
                return JsonResponse({'list':status})
            else:
                return JsonResponse({'list':status})
        else:
            return HttpResponse(request,'none')

    except Exception as e:
        return HttpResponse(request,e)
def upload(request):
    try:
        if request.method == 'POST':
            ayth_storage = pyrebase.initialize_app(config)
            file2 = request.FILES["document"]
            st = ayth_storage.storage()
            cludname = 'photo/' + str(file2)
            st.child(cludname).put(file2)
            URL_IMG = str(st.child(cludname).get_url(None))
            Student.objects.all().delete()
            model = Student.objects.create(url_img=URL_IMG,img_name=cludname)
            model.save()
            return render(request,'home.html',{'img_obj':str(st.child(cludname).get_url(None))})
        else:
            form = UploadFileForm()
        return render(request,'home.html',{'form':form})
    except:
        return render(request,'home.html')


class Home(TemplateView):
    template_name = 'home.html'
    Student.objects.all().delete()