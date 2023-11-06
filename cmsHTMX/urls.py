from django.urls import path

from . import views

urlpatterns = [
    path('', views.cmshtmx_index, name="cmshtmx_index"),
    path('files/', views.get_files, name="cmshtmx_files"),
    path('new/', views.get_post, name="cmshtmx_new"),
    path('edit/<slug:slug>/', views.get_post, name="cmshtmx_edit"),
    path('getsuggestion/', views.get_suggestion, name="cmshtmx_get_suggestion"),

    #path('<slug:slug>/save/', views.save, name='cmshtmx_save'),
    #path('<slug:slug>/unpublish/', views.unpublish, name='cmshtmx_unpublish'),

    #path('<slug:slug>/publish/', views.publish, name='cmshtmx_publish'),
    path('publish/', views.publish, name='cmshtmx_publish'),

    #path('<slug:slug>/savedraft/', views.save_draft, name='cmshtmx_savedraft'),
    path('savedraft/', views.save_draft, name='cmshtmx_savedraft'),

    path('unpublish/', views.unpublish, name='cmshtmx_unpublish'),

    #path('<slug:slug>/save/', views.save, name='cmshtmx_publish_edits'),
    #path('<slug:slug>/save/', views.save, name='cmshtmx_publish_edits'),
    #path('publish/', views.save, name='cmshtmx_publish'),
    #path('new/', views.edit, name='new'),
    #path('new/create/', views.save, name='savenew'),
    #path('ai/', views.writingAssistant, name='writing_assistant'),
    #path('ai/getanswer/', views.getGPTAnswer, name='get_gpt_answer'),
]