from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .spectacular_schema import spectacular_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.urls")),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
]

urlpatterns += spectacular_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
