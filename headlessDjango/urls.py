from django.contrib import admin
from django.urls import include, path
from cms import views

urlpatterns = [
    path("", views.login, name="login"),
    path("cms/", include("cms.urls")),
    path("admin/", admin.site.urls),
]