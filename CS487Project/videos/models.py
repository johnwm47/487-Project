from django.contrib.auth.models import User
from django.db import models
import datetime
from time import strftime
from django.contrib import admin

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

class Comment(models.Model):
        commenter = models.ForeignKey(User)
        replies = models.ManyToManyField('self', related_name='', blank=True)
        content = models.TextField()

        def __unicode__(self):
                return "%s %s %s" % (self.commenter, self.video, self.content)

# instance: the model instance. In this case a Video object. The primary key probably
# will not have been initialized yet, so instance.id cannot be assumed to exist.
def filePath(instance, filename):
        return strftime(instance.title + "%y,%m,%d,%H,%M,%S.mp4")

class Video(models.Model):
        title = models.CharField(max_length=100, unique=True)
        uploader = models.ForeignKey(User)
        description = models.TextField()
        uploadDate = models.DateField(default=datetime.datetime.now(), editable=False)
        viewCount = models.PositiveIntegerField(default=0)
        url = models.URLField()
        authors = models.ManyToManyField(Author)
        keywords = models.ManyToManyField(Keyword)
        journal = models.ForeignKey(Journal)
        video = models.FileField(upload_to=filePath)
        replies = models.ManyToManyField(Comment, related_name='', blank=True)

        def __unicode__(self):
                return self.title

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
        
        class Meta:
            abstract = True

        def __unicode__(self):
            return self.description

class FlagVideo(Flag):
        video = models.ForeignKey(Video, editable=False)

class FlagComment(Flag):
        comment = models.ForeignKey(Comment, editable=False)

# ratings
# related videos
admin.site.register(Comment)
