from django.conf.urls import patterns, url
from videos import views

urlpatterns = patterns('',
                url(r'^$', views.IndexView.as_view(), name='index'),
                url(r'^view/(?P<pk>\d+)/$', views.VideoView.as_view(), name='view'),
                url(r'^view/(?P<pk>\d+)/count$', views.videoCount, name='viewCount'),
                url(r'^search/$', views.searchResult, name='search'),
                url(r'^upload/$', views.uploadFile, name="uploader"),
)
