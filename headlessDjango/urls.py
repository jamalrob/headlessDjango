from django.contrib import admin
from django.urls import include, path
from cms import views

urlpatterns = [
    path("", views.topindex, name="index"),
    path("cms/", include("cms.urls")),
    path("cmshtmx/", include("cmsHTMX.urls")),
    path("admin/", admin.site.urls),
]