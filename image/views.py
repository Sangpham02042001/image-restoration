from django.shortcuts import render, redirect
from wsgiref.util import FileWrapper
from django.http import HttpResponse
import mimetypes
from .form import ImageForm
from .models import Image
import os

# Create your views here.


def index(request):
    if request.method == "POST":
        form = ImageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            obj = form.instance
            return render(request, "index.html", {"obj": obj, "form": ImageForm()})
    else:
        form = ImageForm()
    return render(request, "index.html", {"form": form})


def download_image(request, image_id):
    if request.method == 'GET':
        img = Image.objects.get(unique_id=image_id)
        filePath = './media/images/' + str(img.name)
        # img.file returns full path to the image
        wrapper = FileWrapper(open(filePath, 'rb'))
        content_type = mimetypes.guess_type(
            img.name)[0]  # Use mimetypes to get file type
        print('content_type', content_type)
        response = HttpResponse(wrapper, content_type=content_type)
        response['Content-Length'] = os.path.getsize(filePath)
        response['Content-Disposition'] = "attachment; filename=%s" % img.name
        return response
