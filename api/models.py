from typing import Iterable
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q

# Create your models here.


class Subtitle(models.Model):
    startSecond=models.FloatField()
    endSecond=models.FloatField()
    name=models.CharField(max_length=1000)
    caption=models.TextField(max_length=1000)
    language=models.TextField(max_length=50)


    def get_total_seconds(time: str):
        print(time)
        hrs,minutes,seconds=time.split(":")
        seconds=seconds.split(",")[0]
        hrs,minutes,seconds=int(hrs),int(minutes),int(seconds)
        total=(hrs*60*60)+(minutes*60)+(seconds)
        return total



    def verify(data):
        new_data={
            "name": data.get("name",""),
            "caption": data.get("caption",""),
            "endSecond": data.get("endSecond",-1),
            "startSecond": data.get("startSecond",-1),
            "language": data.get("language","")
        }



        if len(new_data["name"])<1 or len(new_data["name"])>1000:
            raise ValidationError("name should be there.")
        if len(new_data["caption"])<1 or len(new_data["caption"])>1000:
            raise ValidationError("caption should be there.")
        if new_data["endSecond"]<=0:
            raise ValidationError("end Second should be there.")
        if new_data["startSecond"]<0:
            raise ValidationError("start second should be there.")
        if new_data["language"]=="":
            raise ValidationError("language must be there")
        
        
        
        exists=Subtitle.objects.filter(Q(name=new_data["name"]) & Q(Q(endSecond=new_data["endSecond"]) & Q(startSecond=new_data["startSecond"]) & Q(language=new_data["language"]) )).exists()
        if exists:
            raise ValidationError("object already exists")
        
        return new_data
    


