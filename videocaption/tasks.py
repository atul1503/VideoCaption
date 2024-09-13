
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

def extract_subs(filename,video_file_name):
    with open(filename) as f:
        raw=f.read()
        map_list=[]
        instances=raw.split("\n\n")
        for instance in instances:
            try:
                id,time_range,*text=instance.split("\n")
            except ValueError:
                continue
            start_time,end_time=time_range.split(" --> ")
            start_time_seconds=get_seconds(start_time)
            end_time_seconds=get_seconds(end_time)
            map={
                "startTime": start_time_seconds,
                "endTime": end_time_seconds,
                "text": text,
                "name": video_file_name
            }
            map_list.append(map)
    return map_list



@shared_task
def setsubtitles(file_url):
    i=0
    while True: 
        command=["ffmpeg","-i",file_url,"-map","0:s:"+str(i),"file-"+str(i)+".srt"]
        process=subprocess.Popen(command,stderr=open("erro.log","w"),stdout=subprocess.PIPE)
        while True:
            status=process.poll()
            print("status is "+str(status))
            if status!=None:
                print("process is over")
                break
        if status!=0:
            break
        map_list=extract_subs("file-"+str(i)+".srt",file_url+str(i))
        os.remove("file-"+str(i)+".srt")
        for map in map_list:
            name=file_url.split("/")[-1]+"-"+str(i)
            try:
                verified_data=Subtitle.verify(data={
                    "startSecond": map["startTime"],
                    "endSecond": map["endTime"],
                    "caption": map["text"],
                    "name": map["name"]
                })
            except ValidationError:
                print("Data not valid")
                return 

            obj=Subtitle(**verified_data)
            obj.save()

        i=i+1
    print("its done")

