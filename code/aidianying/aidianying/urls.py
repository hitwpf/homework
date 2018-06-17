from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^top$', views.top),
    url(r'^lookup$', views.lookup),
    url(r'^.*$', views.home)
]
