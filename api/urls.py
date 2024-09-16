from django.urls import path,include
from .views import upload_and_process,search_sub,get_file_by_name,poll_status,get_languages,get_current_subtitle

urlpatterns = [
    path("upload_and_process/",upload_and_process),
    path("search_sub_time/",search_sub),
    path("get_file_by_name/",get_file_by_name),
    path("poll_status/",poll_status),
    path("get_lang/",get_languages),
    path("get_current_subtitle/",get_current_subtitle)
]