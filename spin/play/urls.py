from django.urls import path
from . import views

app_name='play'
urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('start', views.StartView.as_view(), name='start'),
]