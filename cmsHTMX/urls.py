from django.urls import path

from . import views

urlpatterns = [
    path('', views.cmshtmx_index, name="cmshtmx_index"),
    path('files/', views.get_files, name="cmshtmx_files"),
    path('edit/<slug:slug>/', views.get_post, name="cmshtmx_edit"),
    path('getsuggestion/', views.get_suggestion, name="cmshtmx_get_suggestion"),
    path('<slug:slug>/save/', views.save, name='cmshtmx_save_draft'),
    #path('new/', views.edit, name='new'),
    #path('new/create/', views.save, name='savenew'),
    #path('ai/', views.writingAssistant, name='writing_assistant'),
    #path('ai/getanswer/', views.getGPTAnswer, name='get_gpt_answer'),
]