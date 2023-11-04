from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('files/', views.getFiles, name="files"),
    #path('edit/<slug:slug>/', views.edit, name="edit"),
    #path('<slug:slug>/save/', views.save, name='save'),
    #path('new/', views.edit, name='new'),
    #path('new/create/', views.save, name='savenew'),
    #path('ai/', views.writingAssistant, name='writing_assistant'),
    #path('ai/getanswer/', views.getGPTAnswer, name='get_gpt_answer'),
]