from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CS487Project.views.home', name='home'),
    # url(r'^CS487Project/', include('CS487Project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^videos/', include('videos.urls', namespace="videos")),
)

if settings.DEBUG:
        urlpatterns += patterns('',
                url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                        'document_root': settings.MEDIA_ROOT,
                }),
                url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
                        'document_root': settings.STATIC_ROOT,
                }),
        )
