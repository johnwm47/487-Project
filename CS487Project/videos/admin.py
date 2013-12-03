from django.contrib import admin
from django.core import urlresolvers
from django.core.exceptions import PermissionDenied
from django.db import router
from videos.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.safestring import mark_safe
from django.views import generic

def blockVideos(q, b=None):
    q.update(block=b)

def block(modeladmin, request, queryset):
    if request.POST.get("reason"):
        blockVideos(queryset, Blocked.objects.get_or_create(reason=request.POST.get("reason"))[0])
        return None
    else:
        opts = modeladmin.model._meta
        app_label = opts.app_label

        context = { 'title': 'Block videos',
                    'queryset': queryset,
                    'opts': opts,
                    'app_label': app_label,
                    'action_checkbox_name': admin.helpers.ACTION_CHECKBOX_NAME
                  }
        return render_to_response('admin/block.html', context, context_instance=RequestContext(request))

def unblock(modeladmin, request, queryset):
    blockVideos(queryset)

class VideoAdmin(admin.ModelAdmin):
        actions=[block, unblock]
        date_hierarchy = 'uploadDate'
        filter_horizontal = ['keywords', 'authors']
        list_display = ('title', 'uploader', 'viewCount', 'url')
        list_filter = ('uploader', 'uploadDate', 'authors', 'keywords', 'journal', "block")
        #inlines = [ FlagAdmin ]
        #exclude = [ Flag ]

class VideoInline(admin.TabularInline):
        model = Video

class KeywordAdmin(admin.ModelAdmin):
        list_display = ['keyword']

class FlagVideoAdmin(admin.ModelAdmin):
        readonly_fields = ['user_link', 'video_link']
        fields = ['user_link', 'video_link', 'description']

        def user_link(self, obj):
            change_url = urlresolvers.reverse('admin:auth_user_change', args=(obj.flagger.id,))
            return mark_safe('<a href="%s">%s</a>' % (change_url, obj.flagger.__str__()))
        user_link.short_description = 'Flagger'

        def video_link(self, obj):
            change_url = urlresolvers.reverse('admin:videos_video_change', args=(obj.video.pk,))
            return mark_safe('<a href="%s">%s</a>' % (change_url, obj.video.__str__()))
        video_link.short_description = 'Video'

class FlagCommentAdmin(admin.ModelAdmin):
        readonly_fields = ['user_link', 'comment_link']
        fields = ['user_link', 'comment_link', 'description']

        def user_link(self, obj):
            change_url = urlresolvers.reverse('admin:auth_user_change', args=(obj.flagger.id,))
            return mark_safe('<a href="%s">%s</a>' % (change_url, obj.flagger.__str__()))
        user_link.short_description = 'Flagger'

        def comment_link(self, obj):
            change_url = urlresolvers.reverse('admin:videos_comment_change', args=(obj.comment.pk,))
            return mark_safe('<a href="%s">%s</a>' % (change_url, obj.comment.__str__()))
        comment_link.short_description = 'Comment'

admin.site.disable_action('delete_selected')
admin.site.register(Video, VideoAdmin)
admin.site.register(Author)
admin.site.register(Journal)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(FlagVideo, FlagVideoAdmin)
admin.site.register(FlagComment, FlagCommentAdmin)
admin.site.register(StarRating)
admin.site.register(BeakerRating)
admin.site.register(VideoView)
admin.site.register(Blocked)
