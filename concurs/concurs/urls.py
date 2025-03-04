from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),
    path(
        "",
        include("events.urls"),
    ),
    path(
        "",
        RedirectView.as_view(url="/history", permanent=False),
        name="homepage",
    ),
]
