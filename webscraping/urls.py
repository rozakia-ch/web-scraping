"""webscraping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from interface import views as viewInter
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/statistik/', viewInter.statistik),
    url(r'^api/condition/', viewInter.condition),
    url(r'^api/getNews/(?P<pk>\d+)/$', viewInter.getNews),
    url(r'^signin', viewInter.login, name='login'),
    url(r'^dashboard/', viewInter.dashboard, name='dashboard'),
    url(r'^berita/', viewInter.berita, name='berita'),
    url(r'^update/(?P<pk>\d+)/$', viewInter.update, name='update'),
    url(r'^delete/(?P<pk>\d+)/$', viewInter.delete, name='delete'),
    url(r'^create/', viewInter.create, name='create'),
    url(r'^test/', viewInter.test),
]

