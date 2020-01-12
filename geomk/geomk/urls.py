from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path("parking/", include("api.urls")),
    path("", lambda request: redirect("parking/", permanent=False)),
]
