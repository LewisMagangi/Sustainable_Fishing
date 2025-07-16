from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import mimetypes
from django.views.static import serve
from django.urls import re_path
from django.views.static import serve as media_serve

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', media_serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]

urlpatterns += [
    re_path(r'^static/(?P<path>.*)$', serve, {
        'document_root': settings.STATIC_ROOT,
    }),
]

