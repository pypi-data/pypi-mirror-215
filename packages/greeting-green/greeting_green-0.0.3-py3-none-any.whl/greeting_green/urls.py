from django.urls import path

from . import views

app_name = "greeting_green"
urlpatterns = [
        path('', views.index, name='index'),
]
