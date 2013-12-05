from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.dispatch import receiver
import datetime
from time import strftime
from django.contrib import admin
import os

from my_comment_app.models import Comment

class Blocked(models.Model):
        reason = models.TextField(unique=True)

        def __unicode__(self):
            return self.reason

# Create your models here.
class Author(models.Model):
        name = models.CharField(max_length=50)

        def __unicode__(self):
                return self.name

class Keyword(models.Model):
        keyword = models.CharField(max_length=100, primary_key=True)

        def __unicode__(self):
                return self.keyword

class Journal(models.Model):
        name = models.CharField(max_length=100)
        year = models.PositiveIntegerField()
        edition = models.PositiveIntegerField()

        def __unicode__(self):
                return "%s %s %s" % (self.name, self.year, self.edition)

# instance: the model instance. In this case a Video object. The primary key probably
# will not have been initialized yet, so instance.id cannot be assumed to exist.
def filePath(instance, filename):
        return strftime(instance.title + "%y%m%d%H%M%S.mp4")

class Video(models.Model):
        title = models.CharField(max_length=100, unique=True)
        uploader = models.ForeignKey(User)
        description = models.TextField()
        uploadDate = models.DateField(default=datetime.datetime.now(), editable=False)
        viewCount = models.PositiveIntegerField(default=0)
        url = models.URLField()
        authors = models.ManyToManyField(Author, blank=True)
        keywords = models.ManyToManyField(Keyword, blank=True)
        journal = models.ForeignKey(Journal)
        video = models.FileField(upload_to=filePath)
        block = models.ForeignKey(Blocked, related_name='', blank=True, null=True, default=None, on_delete=models.SET_NULL)

        def __unicode__(self):
                return self.title
        
        def get_absolute_url(self):
            return reverse('videos:view', args=(self.id,))

@receiver(models.signals.pre_save, sender=Video)
def fileCleanup(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old = Video.objects.get(pk=instance.pk).video
    except Video.DoesNotExist:
        return False

    new = instance.video
    if not old == new:
        if os.path.isfile(old.path):
            os.remove(old.path)

@receiver(models.signals.post_delete, sender=Video)
def fileCleanupOnDelete(sender, instance, **kwargs):
    if instance.video:
        if os.path.isfile(instance.video.path):
            os.remove(instance.video.path)

class Rating(models.Model):
        rater = models.ForeignKey(User)
        rating = models.PositiveIntegerField(choices=[ (1, 'One'),
                                                       (2, 'Two'),
                                                       (3, 'Three'),
                                                       (4, 'Four'),
                                                       (5, 'Five'),
                                                     ],
                                             )

        class Meta:
            abstract = True

        def __unicode__(self):
                return "%s" % (self.rating)
        
class BeakerRating(Rating):
        video = models.ForeignKey(Video, related_name='beakers')

class StarRating(Rating):
        video = models.ForeignKey(Video, related_name='stars')

class Flag(models.Model):
        flagger = models.ForeignKey(User, editable=False)
        description = models.TextField()
        resolved = models.BooleanField(default=False)
        
        class Meta:
            abstract = True

        def __unicode__(self):
            return self.description

class FlagVideo(Flag):
        video = models.ForeignKey(Video, editable=False)

class FlagComment(Flag):
        comment = models.ForeignKey(Comment, editable=False)

class View(models.Model):
        user = models.ForeignKey(User)
        count = models.PositiveIntegerField(default=0)

        class Meta:
            abstract = True

class VideoView(View):
        video = models.ForeignKey(Video, related_name='user_views')

class CommentVideo(Comment):
        video = models.ForeignKey(Video)
        class Meta:
            abstract = True

admin.site.register(Comment)
