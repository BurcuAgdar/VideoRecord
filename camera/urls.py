from django.contrib import admin
from django.urls import path
from video.views import Home, home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home_view'),
    path('home/', Home, name='Home')
]
