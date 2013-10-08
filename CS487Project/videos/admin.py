from django.contrib import admin
from videos.models import Video, Author, Journal, Keyword

admin.site.register(Video)
admin.site.register(Author)
admin.site.register(Journal)
admin.site.register(Keyword)
