
import subprocess
from celery import shared_task
from api.models import Subtitle
from django.core.exceptions import ValidationError
import os
import json

@shared_task
def hello_task():
    return 2+2


def get_seconds(time: str):
    hrs,minutes,seconds=time.split(":")
    seconds=seconds.split(",")[0]
    hrs,minutes,seconds=int(hrs),int(minutes),int(seconds)
    total=(hrs*60*60)+(minutes*60)+(seconds)
    return total


def get_subtitle_languages(file_name):

    command=['ffprobe', '-print_format', 'json' ,'-show_format', '-show_streams', file_name]
    
    result = subprocess.run(command, capture_output=True, text=True)

    print("output is this"+result.stdout)
    print("error is this"+result.stderr)

    process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    while True:
        status=process.poll()
        if status!=None:
            break
    output,err=process.communicate()
    data=json.loads(output)
    langs=[]
    index=0
    for stream in data["streams"]:
        if stream["codec_type"]=="subtitle":
            langs.append([index,stream["tags"].get("language","UnknownLanguage")])
            index+=1
    return langs



def extract_subs(filename,video_file_name,lang):
    with open(filename) as f:
        raw=f.read()
        map_list=[]
        instances=raw.split("\n\n")
        for instance in instances:
            try:
                id,time_range,*text=instance.split("\n")
                if type(text) == list:
                    text="\n".join(text)
            except ValueError:
                continue
            start_time,end_time=time_range.split(" --> ")
            start_time_seconds=get_seconds(start_time)
            end_time_seconds=get_seconds(end_time)
            map={
                "startTime": start_time_seconds,
                "endTime": end_time_seconds,
                "text": text,
                "name": video_file_name,
                "language": lang
            }
            map_list.append(map)
    return map_list



@shared_task
def setsubtitles(file_url):
    
    languages=get_subtitle_languages(file_url)
    for index,lang in languages:
        command=["ffmpeg","-i",file_url,"-map","0:s:"+str(index),"file-"+str(lang)+".srt"]
        process=subprocess.Popen(command,stderr=open("erro.log","w"),stdout=subprocess.PIPE)
        while True:
            status=process.poll()
            print("Subtitle stream processing status : "+str(status))
            if status!=None:
                print("A substitle stream processing is over")
                break
        if status!=0:
            break
        map_list=extract_subs("file-"+str(lang)+".srt",file_url,lang)
        os.remove("file-"+str(lang)+".srt")
        for map in map_list:
            name=file_url.split("/")[-1]+"-"+str(lang)
            try:
                verified_data=Subtitle.verify(data={
                    "startSecond": map["startTime"],
                    "endSecond": map["endTime"],
                    "caption": map["text"],
                    "name": map["name"],
                    "language": map["language"]
                })
            except ValidationError:
                print("Data not valid")
                continue

            obj=Subtitle(**verified_data)
            obj.save()
    print("All subs processed.")

