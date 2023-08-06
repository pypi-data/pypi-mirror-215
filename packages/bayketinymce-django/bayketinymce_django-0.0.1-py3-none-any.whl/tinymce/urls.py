from django.urls import path
from . import views

app_name = "tinymce"

urlpatterns = [
    path("upload-image/", views.TinyMCEImageUpload.as_view(), name="tinymce-upload-image")
]
