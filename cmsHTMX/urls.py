from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('files/', views.get_files, name="files"),
    path('edit/<slug:slug>/', views.get_post, name="get_post"),
    #path('<slug:slug>/save/', views.save, name='save'),
    #path('new/', views.edit, name='new'),
    #path('new/create/', views.save, name='savenew'),
    #path('ai/', views.writingAssistant, name='writing_assistant'),
    #path('ai/getanswer/', views.getGPTAnswer, name='get_gpt_answer'),
]