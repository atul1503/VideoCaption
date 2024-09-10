from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q

# Create your models here.


class Subtitle(models.Model):
    startSecond=models.FloatField()
    endSecond=models.FloatField()
    name=models.CharField(max_length=1000)
    caption=models.TextField(max_length=1000)

    def verify(self,data):
        new_data={
            "name": data.get("name",""),
            "caption": data.get("caption",""),
            "endSecond": data.get("endSecond",-1),
            "startSecond": data.get("startSecond",-1)
        }

        if len(new_data["name"])<1 or len(new_data["name"])>1000:
            raise ValidationError("name should be there.")
        if len(new_data["caption"])<1 or len(new_data["caption"])>1000:
            raise ValidationError("caption should be there.")
        if new_data["endSecond"]<=0:
            raise ValidationError("end Second should be there.")
        if new_data["startSecond"]<0:
            raise ValidationError("start second should be there.")
        
        exists=Subtitle.objects.filter(Q(name=new_data["name"]) & Q(Q(endSecond__lt=new_data["endSecond"]) | Q(startSecond=new_data["endSecond"]) ) & Q(Q(startSecond__gt=new_data["startSecond"]) | Q(startSecond=new_data["startSecond"]) ) ).exists()
        if exists:
            raise ValidationError("object already exists")
        
        return new_data
    


