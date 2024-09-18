from django.shortcuts import render
from django.http import JsonResponse,HttpRequest,FileResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings
from api.models import Subtitle
from videocaption.tasks import setsubtitles
import videocaption.settings
from django.views.decorators.csrf import csrf_exempt
from celery.result import AsyncResult
import shutil
import json


# Create your views here.

@csrf_exempt
def search_sub(request: HttpRequest):
    body=json.loads(request.body)
    text: str=body.get("text",None)
    video_name: str=body.get("video_name","")
    obj=Subtitle.objects.filter(caption__icontains=text,name=video_name)
    return JsonResponse({
        "subtitle": list(obj.values())
    })

def get_current_subtitle(request):
    time=abs(int(float(request.GET.get("time",0))))
    video_name=request.GET.get("video_name",0)
    language=request.GET.get("language","")
    video_path=os.path.join(settings.MEDIA_ROOT,video_name)
    obj=Subtitle.objects.filter(
        Q(name=video_path) 
        &
        Q(language=language)
        &
        Q( 
            Q(startSecond__lt=time) | Q(startSecond=time)
         )
         &
        Q(
            Q(endSecond__gt=time) | Q(endSecond=time)
        )
        )
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
    response=FileResponse(open(os.path.join(settings.MEDIA_ROOT,name),"rb"),content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{name}"'
    response['Content-Length'] = os.path.getsize(os.path.join(settings.MEDIA_ROOT,name))
    return response

    
@csrf_exempt
def get_languages(request: HttpRequest):
    qs=Subtitle.objects.filter(name=request.GET["video_name"]).distinct("language")
    return JsonResponse({
        "subtitles": list(qs.values())
    })


def get_file_object(file):
    *firstnames,extension=file.name.split(".")
    if type(firstnames)==list:
        firstnames=".".join(firstnames)
    if extension=="mkv":
        extension="mp4"
    file.name=firstnames+"."+extension
    return file

@csrf_exempt
def upload_and_process(request):
    file=request.FILES['file']
    file=get_file_object(file)
    if os.path.exists(os.path.join(settings.MEDIA_ROOT,file.name)):
        return JsonResponse({
            "task_id": 0, 
            "message": "File already exists"
        },status=201)
    
    
    file_name=default_storage.save(file.name,ContentFile(file.read()))
    file_url=os.path.join(settings.MEDIA_ROOT,file_name)
    task_id=setsubtitles.delay(file_url)
    return JsonResponse({
        "task_id": task_id.id
    },status=200)
    
def get_all_files(request):
    query_set=Subtitle.objects.order_by('name').distinct('name')
    return JsonResponse({
       "subtitles":list(query_set.values())
    })
    

