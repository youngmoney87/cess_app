from django.urls import path
from raw_data import views

urlpatterns = [
    path("data/<name>", views.data, name="coded"),
    path("main2", views.main2),
]