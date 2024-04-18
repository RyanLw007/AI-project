from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.chat_interface, name='chat_interface'),
    path('get_response/', views.get_response, name='get_response')

]