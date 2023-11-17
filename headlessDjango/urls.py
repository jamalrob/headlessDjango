from django.contrib import admin
from django.urls import include, path
from cmsHTMX import views

urlpatterns = [
    path("", views.cmshtmx_index, name="index"),
    path("cmshtmx/", include("cmsHTMX.urls")),
    path("admin/", admin.site.urls),
]