from django.urls import path
from .views import upload_reference, upload_check_image, upload_check_video,choose,login,logout,signup


urlpatterns = [
    path('signup/',signup, name='signup'),
    path('', login, name='login'),
    path('logout/',logout, name='logout'),
    path("upload-reference/", upload_reference, name="upload_reference"),
    path("upload-image-check/", upload_check_image, name="upload_check_image"),
    path("upload-video-check/", upload_check_video, name="upload_check_video"),
    path("choose/",choose,name="choose"),
    
]