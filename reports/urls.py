from django.urls import path
from . import views
from django.contrib.auth import login


urlpatterns = [
    path("", views.home),
    path("login/", login, {'template_name': 'reports/login.html'}),
    path("report/", views.reportchoice),
    path("main/", views.main_report),
]
