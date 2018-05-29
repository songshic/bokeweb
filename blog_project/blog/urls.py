# Author:song
from django.conf.urls import url
from .views import  *
from .upload import *
urlpatterns = [
    url(r'^$',index,name='index'),
    url(r'^index/$',index,name='index'),
    url(r'^archive/$',archive,name='archive'),
    url(r'^article/$',article,name='article'),
    url(r'^reg', do_reg, name='reg'),
    url(r'^login', do_login, name='login'),
    url(r'^logout$', do_logout, name='logout'),
    url(r'^comment/post/$', comment_post, name='comment_post'),
]
