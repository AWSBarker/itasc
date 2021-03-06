from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('itasc.urls', namespace='dashboard')),
    path('itasc/', include('itasc.urls', namespace='itasc')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
