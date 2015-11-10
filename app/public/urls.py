from django.conf.urls import url

from public import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
