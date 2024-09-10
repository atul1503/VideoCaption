from django.urls import path,include


urlpatterns = [
    path("upload_and_process/",upload_and_process)
    path("search_sub_time/",search_sub)
]