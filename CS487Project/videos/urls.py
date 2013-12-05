from django.conf.urls import patterns, url
from videos import views

urlpatterns = patterns('',
                url(r'^$', views.IndexView.as_view(), name='index'),
                url(r'^view/(?P<pk>\d+)/$', views.ViewVideo.as_view(), name='view'),
                url(r'^view/(?P<pk>\d+)/count$', views.videoCount, name='viewCount'),
                url(r'^view/(?P<pk>\d+)/edit$', views.EditVideo.as_view(), name='editVideo'),
                url(r'^search/$', views.searchResult, name='search'),
                url(r'^upload/$', views.uploadFile, name="uploader"),
                url(r'^video/(?P<pk>\d+)/flag$', views.createVideoFlag, name="flagVideo"),
                url(r'^comment/(?P<pk>\d+)/flag$', views.createCommentFlag, name="flagComment"),
                url(r'^video/(?P<pk>\d+)/rating/(?P<t>\w+)/$', views.createRating, name="createRating"),
				
)
