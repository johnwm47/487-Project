from django.conf.urls import patterns, url
from django.views import generic
from videos.models import Video

urlpatterns = patterns('',
                url(r'^view/(?P<pk>\d+)/$', generic.DetailView.as_view(template_name="videos/view.html", model=Video), name='view'),
#                url(r'^search/<query>/$', , name='search'),
)
