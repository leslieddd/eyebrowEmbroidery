from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import CustomerFace, PostSimFace, EyeBrowFace
from subprocess import run
from webcam import image_capture
from geometric_shape import golden_ratio
from eyebrow_test import put_that_eyebrow
from Store_Image import insertBLOB
import os
import sys
import cv2
import re
import os.path
import time
from os import path




def home(request):
    if request.method == "POST" and "webcam" in request.POST:
        CustomerFace.objects.all().delete()
        name = request.POST.get('cust_name', None)
        if name == "":
            messages.warning(request, f'Please enter your name!')
            return redirect('main-home')
        else:
            # dirname = "main\static\main\customer"
            dirname = '/Users/dongyirui/Desktop/eyebrows/main/static/main/customer'
            if len(os.listdir(dirname)) > 0:
                for f in os.listdir(dirname):
                    os.remove(os.path.join(dirname, f))

            image_capture(name)
            CustomerFace(cust_name=name, cust_face=os.listdir(dirname)[0]).save()
            ###
            """if len(os.listdir(dirname)) == 0:
                messages.warning(request, f'Please upload a frontal face image!')
                return redirect('main-home')
            ###"""
            # CustomerFace(cust_name=name, cust_face=os.listdir(dirname)).save()
            messages.success
            messages.success(request, f'File Uploaded!')
            return redirect('main-home')
##############
    if request.method == "POST" and "uploadfile" in request.POST:
        CustomerFace.objects.all().delete()
        nameholder = request.POST.get('cust_name', None)
        if nameholder == "":
            messages.warning(request, f'Please enter your name!')
            return redirect('main-home')
        else:
            if len(request.FILES) == 0:
                messages.warning(request, f'please upload a proper image before processing')
                return redirect('main-home')
            myfile = request.FILES['imagecontent']
            # dirname = "main\static\main\customer"
            dirname = '/Users/dongyirui/Desktop/eyebrows/main/static/main/customer'
            fs = FileSystemStorage(dirname)

            if len(os.listdir(dirname)) > 0:
                for f in os.listdir(dirname):
                    os.remove(os.path.join(dirname, f))

            filename = fs.save(myfile.name, myfile)
            src = dirname + "/" + myfile.name
            dst = dirname + "/" + str(nameholder) + ".jpg"
            os.rename(src, dst)

            CustomerFace(cust_name=nameholder, cust_face=os.listdir(dirname)[0]).save()
            # CustomerFace(cust_name=nameholder, cust_face=os.listdir(dirname)).save()


            messages.success(request, f'File Uploaded!')
            return redirect('main-home')

    context = {
        'cust': CustomerFace.objects.all(),
    }

    return render(request, '/Users/dongyirui/Desktop/eyebrows/main/templates/main/home.html', context)


def eyebrowSim(request):
    path, dirs, files = next(os.walk("/Users/dongyirui/Desktop/eyebrows/main/static/main/img"))
    # path, dirs, files = next(os.walk("/home/python/Desktop/eyebrows/eyebrows/main/static/main/img"))
    img_count = len(files)
    print("tag    ", img_count)
    if img_count == 0:
        messages.warning(request, f'Please enter your name!')
        return redirect('main-home')

    if request.method == "POST" and "proceed" in request.POST:
        # path = 'main\static\main\customer'
        path = '/Users/dongyirui/Desktop/eyebrows/main/static/main/customer'
        dirname = path + "/" + os.listdir(path)[0]
        name = re.sub("[.].*", "", str(os.listdir(path)[0]))

        # path = 'main\static\main\PostSim'
        path = '/Users/dongyirui/Desktop/eyebrows/main/static/main/PostSim'
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))

        golden_ratio(dirname, str(name))

        if len(os.listdir(path)) == 0:
            messages.warning(request, f'Please upload a frontal face image!')
            return redirect('main-home')


        PostSimFace.objects.all().delete()
        PostSimFace(postsim_name=name, postsim_face=os.listdir(path)[0]).save()


    context = {
        'postcust': PostSimFace.objects.all(),
        'imgcount': range(img_count),
        'cust': CustomerFace.objects.all(),
    }

    if request.method == "POST" and "back" in request.POST:
        # return render(request, 'main/eyebrowSim.html', context)
        return render(request, '/Users/dongyirui/Desktop/eyebrows/main/templates/main/eyebrowSim.html', context)

    if request.method == "POST" and "saveBtn" in request.POST:
        print("saveBtn - test")

        path = '/Users/dongyirui/Desktop/eyebrows/main/static/main/eyebrow'
        name = re.sub("[.].*", "", str(os.listdir(path)[0]))
        storeiamge=path + "/" + name + ".jpg"

        print('TAG storeImage:' + storeiamge)
        print('TAG name:' + name)
        if (os.path.exists(storeiamge)):
            insertBLOB(str(name), storeiamge)
            messages.success(request, f'Save Successfully')
        else:
            messages.warning(request, f'Save Failed')

        time.sleep(3)
     ###999
        context = {
            'cust': CustomerFace.objects.all(),
            'eyebrowcust': EyeBrowFace.objects.all(),
        }
        return render(request, '/Users/dongyirui/Desktop/eyebrows/main/templates/main/eyebrowResult.html', context)
    return render(request, '/Users/dongyirui/Desktop/eyebrows/main/templates/main/eyebrowSim.html', context)
      ###999

def eyebrowResult(request):
    if request.method == "POST" and "eyebrow" in request.POST:
        eyebrow_id = request.POST.get("eyebrow", None)
        eyebrow_img_path = "/Users/dongyirui/Desktop/eyebrows/main/static/main/img/" + str(eyebrow_id) + "eyebrow.png"
        # eyebrow_img_path = "/home/python/Desktop/eyebrows/eyebrows/main/static/main/img" + str(eyebrow_id) + "eyebrow.png"
        # path = 'main\static\main\customer'
        path = '/Users/dongyirui/Desktop/eyebrows/main/static/main/customer'
        dirname = path + "/" + os.listdir(path)[0]
        name = re.sub("[.].*", "", str(os.listdir(path)[0]))

        # path = 'main\static\main\eyebrow'
        path = '/Users/dongyirui/Desktop/eyebrows/main/static/main/eyebrow'
        storeiamge=path + "/" + name + "_eyebrow.jpg"
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))

        put_that_eyebrow(dirname, eyebrow_img_path, str(name))

        EyeBrowFace.objects.all().delete()
        EyeBrowFace(eyebrow_name=name, eyebrow_face=os.listdir(path)[0]).save()
        #if (os.path.exists(storeiamge)):
               #insertBLOB(str(name), storeiamge)



    context = {
        'cust': CustomerFace.objects.all(),
        'eyebrowcust': EyeBrowFace.objects.all(),
    }

    return render(request, '/Users/dongyirui/Desktop/eyebrows/main/templates/main/eyebrowResult.html', context)


"""from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import CustomerFace, PostSimFace, EyeBrowFace
from subprocess import run
from webcam import image_capture
from geometric_shape import golden_ratio
from eyebrow_test import put_that_eyebrow
import os
import sys
import cv2
import re


def home(request):
    if request.method == "POST" and "webcam" in request.POST:
        CustomerFace.objects.all().delete()
        name = request.POST.get('cust_name', None)
        if name == "":
            messages.warning(request, f'Please enter your name!')
            return redirect('main-home')
        else:
            # dirname = "main\static\main\customer"
            dirname = '/Users/dongyirui/Desktop/eyebrows/main/static/main/customer'
            if len(os.listdir(dirname)) > 0:
                for f in os.listdir(dirname):
                    os.remove(os.path.join(dirname, f))

            image_capture(name)
            CustomerFace(cust_name=name, cust_face=os.listdir(dirname)[0]).save()
            # CustomerFace(cust_name=name, cust_face=os.listdir(dirname)).save()
            messages.success
            messages.success(request, f'File Uploaded!')
            return redirect('main-home')
##############
    if request.method == "POST" and "uploadfile" in request.POST:
        CustomerFace.objects.all().delete()
        nameholder = request.POST.get('cust_name', None)
        if nameholder == "":
            messages.warning(request, f'Please enter your name!')
            return redirect('main-home')
        else:
            myfile = request.FILES['imagecontent']
            # dirname = "main\static\main\customer"
            dirname = '/Users/dongyirui/Desktop/eyebrows/main/static/main/customer'
            fs = FileSystemStorage(dirname)

            if len(os.listdir(dirname)) > 0:
                for f in os.listdir(dirname):
                    os.remove(os.path.join(dirname, f))

            filename = fs.save(myfile.name, myfile)
            src = dirname + "/" + myfile.name
            dst = dirname + "/" + str(nameholder) + ".jpg"
            os.rename(src, dst)

            CustomerFace(cust_name=nameholder, cust_face=os.listdir(dirname)[0]).save()
            # CustomerFace(cust_name=nameholder, cust_face=os.listdir(dirname)).save()


            messages.success(request, f'File Uploaded!')
            return redirect('main-home')

    context = {
        'cust': CustomerFace.objects.all(),
    }

    return render(request, '/Users/dongyirui/Desktop/eyebrows/main/templates/main/home.html', context)

    
def eyebrowSim(request):
    path, dirs, files = next(os.walk("/Users/dongyirui/Desktop/eyebrows/main/static/main/img"))
    # path, dirs, files = next(os.walk("/home/python/Desktop/eyebrows/eyebrows/main/static/main/img"))
    img_count = len(files)
    if request.method == "POST" and "proceed" in request.POST:
        # path = 'main\static\main\customer'
        path = '/Users/dongyirui/Desktop/eyebrows/main/static/main/customer'
        dirname = path + "/" + os.listdir(path)[0]
        name = re.sub("[.].*", "", str(os.listdir(path)[0]))

        # path = 'main\static\main\PostSim'
        path = '/Users/dongyirui/Desktop/eyebrows/main/static/main/PostSim'
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))
    
        golden_ratio(dirname, str(name))

        PostSimFace.objects.all().delete()
        PostSimFace(postsim_name=name, postsim_face=os.listdir(path)[0]).save()

    
    context = {
        'postcust': PostSimFace.objects.all(),
        'imgcount': range(img_count),
        'cust': CustomerFace.objects.all(),
    }

    if request.method == "POST" and "back" in request.POST:
        # return render(request, 'main/eyebrowSim.html', context)
        return render(request, '/Users/dongyirui/Desktop/eyebrows/main/templates/main/eyebrowSim.html', context)


    return render(request, '/Users/dongyirui/Desktop/eyebrows/main/templates/main/eyebrowSim.html', context)


def eyebrowResult(request):
    if request.method == "POST" and "eyebrow" in request.POST:
        eyebrow_id = request.POST.get("eyebrow", None)
        eyebrow_img_path = "/Users/dongyirui/Desktop/eyebrows/main/static/main/img/" + str(eyebrow_id) + "eyebrow.png"
        # eyebrow_img_path = "/home/python/Desktop/eyebrows/eyebrows/main/static/main/img" + str(eyebrow_id) + "eyebrow.png"
        # path = 'main\static\main\customer'
        path = '/Users/dongyirui/Desktop/eyebrows/main/static/main/customer'
        dirname = path + "/" + os.listdir(path)[0]
        name = re.sub("[.].*", "", str(os.listdir(path)[0]))

        # path = 'main\static\main\eyebrow'
        path = '/Users/dongyirui/Desktop/eyebrows/main/static/main/eyebrow'
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))

        put_that_eyebrow(dirname, eyebrow_img_path, str(name))

        EyeBrowFace.objects.all().delete()
        EyeBrowFace(eyebrow_name=name, eyebrow_face=os.listdir(path)[0]).save()

    context = {
        'cust': CustomerFace.objects.all(),
        'eyebrowcust': EyeBrowFace.objects.all(),
    }

    return render(request, '/Users/dongyirui/Desktop/eyebrows/main/templates/main/eyebrowResult.html', context)"""