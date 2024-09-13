from django.shortcuts import render
from django.http import JsonResponse,HttpRequest,FileResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.http import JsonResponse
from django.conf import settings
from api.models import Subtitle
from videocaption.tasks import setsubtitles
import videocaption.settings
from django.views.decorators.csrf import csrf_exempt
from celery.result import AsyncResult


# Create your views here.


def search_sub(request: HttpRequest):
    text: str=request.body.get("text",None)
    obj=Subtitle.objects.filter(caption__icontains=text)
    return JsonResponse({
        "subtitle": obj
    })

def poll_status(request: HttpRequest):
    id=request.GET.get("id","")
    return JsonResponse({
        "status" : AsyncResult(id).status
        })


def get_file_by_name(request: HttpRequest):
    name=request.GET.get("name","")
    return FileResponse(open(os.path.join(settings.MEDIA_URL,name),"rb"))
    

@csrf_exempt
def upload_and_process(request):
    file=request.FILES['file']
    file_name=default_storage.save(file.name,ContentFile(file.read()))
    file_url=os.path.join(settings.MEDIA_URL,file_name)[1:]
    task_id=setsubtitles.delay(file_url)
    return JsonResponse({
        "task_id": task_id.id
    })
    
    

