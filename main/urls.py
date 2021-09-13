from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from users.views import index
from main import settings


urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('profiles/', include('users.urls')),
    path('wall/', include('wall.urls')),
    path('followers/', include('followers.urls')),
    path('feed/', include('feed.urls')),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
