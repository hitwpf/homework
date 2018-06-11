from django.conf.urls import url

from demo import views

urlpatterns = [
    url(r'^home$', views.home),
    url(r'^add$', views.add),
    url(r'^.*$', views.hello)
]
