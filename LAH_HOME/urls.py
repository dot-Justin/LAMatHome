from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('LAH_HOME_APP_MAIN.urls', namespace='main')),
    path('users/', include('LAH_USER.urls', namespace='users')),
]
