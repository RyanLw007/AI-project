from django.urls import path
from . import views#, NLP2


urlpatterns = [
    
    path('', views.chat_interface, name='chat_interface'),
    path('get_response/', views.get_response, name='get_response')
    #path('get_response/',NLP2, name='get_response')
]