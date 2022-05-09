from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('htmx.urls')),
    path('', include('country.urls'))
]
