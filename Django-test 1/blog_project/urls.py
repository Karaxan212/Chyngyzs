from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
    path("crud/", include("crud.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("tours/", include("tours.urls")),
]
