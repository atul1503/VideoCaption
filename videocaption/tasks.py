
import subprocess
from celery import shared_task
from api.models import Subtitle
from django.core.exceptions import ValidationError
import os

@shared_task
def hello_task():
    return 2+2


def get_seconds(time: str):
    hrs,minutes,seconds=time.split(":")
    seconds=seconds.split(",")[0]
    hrs,minutes,seconds=int(hrs),int(minutes),int(seconds)
    total=(hrs*60*60)+(minutes*60)+(seconds)
    return total

def extract_subs(filename):
    with open(filename) as f:
        raw=f.read()
        map_list=[]
        instances=raw.split("\n\n")
        for instance in instances:
            id,time_range,text=instance.split("\n")
            start_time,end_time=time_range.split(" --> ")
            start_time_seconds=get_seconds(start_time)
            end_time_seconds=get_seconds(end_time)
            map={
                "startTime": start_time_seconds,
                "endTime": end_time_seconds,
                "text": text
            }
            map_list.append(map)
    return map_list



@shared_task
def setsubtitles(file_url):

    i=0
    while True: 
        command=["ffmpeg","-i",file_url,"-map","file-"+i+".srt"]
        process=subprocess.Popen(command,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
        while True:
            status=process.poll()
            if status!=None:
                break
        if status!=0:
            break
        map_list=extract_subs("file-"+i+".srt")
        os.remove("file-"+i+".srt")
        for map in map_list:
            name=file_url.split("/")[-1]+"-"+i
            try:
                verified_data=Subtitle.verify({
                    "startSecond": map["startTime"],
                    "endSecond": map["endTime"],
                    "caption": map["text"],
                    "name": map["name"]
                })
            except ValidationError:
                return 

            obj=Subtitle(**verified_data)
            obj.save()

        i=i+1

