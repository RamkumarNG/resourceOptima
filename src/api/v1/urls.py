from django.urls import re_path, include

urlpatterns = [
    re_path(r"v1/", include("api.v1.manager.urls")),
    re_path(r"v1/", include("api.v1.resource.urls")),
    re_path(r"v1/", include("api.v1.project.urls")),
]
