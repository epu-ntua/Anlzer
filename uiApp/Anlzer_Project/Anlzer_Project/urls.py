from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
import os

urlpatterns = [
    url(r'^anlzer/', include('anlzer.urls')),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if os.environ.get('LOGNAME')=='mpetyx':
    urlpatterns = urlpatterns + [url(r'^api/', include('api.urls'))]