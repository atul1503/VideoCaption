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
import json


# Create your views here.

@csrf_exempt
def search_sub(request: HttpRequest):
    body=json.loads(request.body)
    text: str=body.get("text",None)
    obj=Subtitle.objects.filter(caption__icontains=text)
    return JsonResponse({
        "subtitle": list(obj.values())
    })

def poll_status(request: HttpRequest):
    id=request.GET.get("id","")
    return JsonResponse({
        "status" : AsyncResult(id).status
        })

@csrf_exempt
def get_file_by_name(request: HttpRequest):
    name=request.GET.get("name","")
    return FileResponse(open(os.path.join(settings.MEDIA_ROOT,name),"rb"))
    

@csrf_exempt
def upload_and_process(request):
    file=request.FILES['file']

    if os.path.exists(os.path.join(settings.MEDIA_ROOT,file.name)):
        return JsonResponse({
            "task_id": "", 
            "message": "File already exists"
        },status=201)

    file_name=default_storage.save(file.name,ContentFile(file.read()))
    file_url=os.path.join(settings.MEDIA_ROOT,file_name)
    task_id=setsubtitles.delay(file_url)
    return JsonResponse({
        "task_id": task_id.id
    },status=200)
    
    

