"""limber URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from app import views

app_name = 'app'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/', include('app.urls')),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^login/', views.login, name='login'),
    url(r'^dashboard/', views.dashboard, name='dashboard'),
    url(r'^comfirm/', views.comfirm_view, name='comfirm'),
    url(r'^projects/$', views.create_project, name='create_project'),
    url(r'^projects/(?P<invite_code>[0-9a-zA-Z]+)/$', views.respond_project_invite, name='project_invite'),
    url(
    r'^password/reset/complete/(?P<reset_code>[0-9a-zA-Z]+)/$',
    views.respond_password_reset,
    name='password_reset'),
]
