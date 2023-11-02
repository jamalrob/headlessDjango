from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('edit/<slug:slug>/', views.edit, name="edit"),
    path('<slug:slug>/save/', views.save, name='save'),
]