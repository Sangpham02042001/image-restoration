
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("images/<uuid:image_id>/download",
         views.download_image, name="download_image")
]
