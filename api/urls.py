from django.urls import path,include
from .views import upload_and_process,search_sub,get_file_by_name,poll_status

urlpatterns = [
    path("upload_and_process/",upload_and_process),
    path("search_sub_time/",search_sub),
    path("get_file_by_name/",get_file_by_name),
    path("poll_status/",poll_status)
]