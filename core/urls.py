from django.conf import settings
from django.conf.urls.i18n import i18n_patterns  # noqa: F401
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from apps.shared.views.base import (
    custom_handler404,
    custom_handler500,
    custom_handler403,
    custom_handler400,
)
from core.config.swagger import urlpatterns as swagger_patterns

urlpatterns = (
    [
        path("i18n/", include("django.conf.urls.i18n")),
    ]
    + i18n_patterns(
        path("admin/", admin.site.urls),
    )
    + [
        path("", include("apps.shared.urls")),
        path("api/v1/users/", include("apps.users.urls")),
        path("api/v1/shop/", include("apps.shop.urls")),
        path("rosetta/", include("rosetta.urls")),
        # Media and static files
        re_path(r"static/(?P<path>.*)", serve, {"document_root": settings.STATIC_ROOT}),
        re_path(r"media/(?P<path>.*)", serve, {"document_root": settings.MEDIA_ROOT}),
    ]
)

urlpatterns += swagger_patterns
if not settings.DEBUG:
    handler404 = custom_handler404
    handler500 = custom_handler500
    handler403 = custom_handler403
    handler400 = custom_handler400
