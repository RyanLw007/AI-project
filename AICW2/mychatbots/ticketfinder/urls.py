from django.urls import path
from . import views#, NLP2


urlpatterns = [
    
    path('', views.chat_interface, name='chat_interface'),
    path('get_response/', views.get_response, name='get_response'),
    path('results/', views.train_view, name='train_results'),
    path('clear_json/', views.clear_json, name='clear_json'),
    #path('get_response/',NLP2, name='get_response')
]