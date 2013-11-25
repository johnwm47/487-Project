from django.contrib import admin
from videos.models import Video, Author, Journal, Keyword, Flag

class FlagAdmin(admin.TabularInline):
    model = Video.flags.through

class VideoAdmin(admin.ModelAdmin):
        date_hierarchy = 'uploadDate'
        filter_horizontal = ['keywords', 'authors']
        list_display = ('title', 'uploader', 'viewCount', 'url')
        list_filter = ('uploader', 'uploadDate', 'authors', 'keywords', 'journal')
        inlines = [ FlagAdmin ]
        exclude = [ Flag ]

class KeywordAdmin(admin.ModelAdmin):
        list_display = ['keyword']
        
admin.site.register(Video, VideoAdmin)
admin.site.register(Author)
admin.site.register(Journal)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Flag)
