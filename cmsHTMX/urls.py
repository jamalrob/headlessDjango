from django.urls import path

from . import views

urlpatterns = [
    path('', views.cmshtmx_index, name="cmshtmx_index"),
    path('files/', views.get_files, name="cmshtmx_files"),
    path('new/', views.get_post, name="cmshtmx_new"),
    path('edit/<slug:slug>/', views.get_post, name="cmshtmx_edit"),
    path('getsuggestion/', views.get_suggestion, name="cmshtmx_get_suggestion"),
    path('publish/', views.publish, name='cmshtmx_publish'),
    path('savedraft/', views.save_draft, name='cmshtmx_savedraft'),
    path('unpublish/', views.save_draft, name='cmshtmx_unpublish'),
]