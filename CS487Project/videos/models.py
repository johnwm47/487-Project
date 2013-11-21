from django.contrib.auth.models import User
from django.db import models
import datetime
from time import strftime
from django.contrib import admin

class Flag(models.Model):
        flagger = models.ForeignKey(User)
        description = models.TextField()

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
        replies = models.ManyToManyField('self', related_name='')
        content = models.TextField()
        flags = models.ManyToManyField(Flag, related_name='')

        def __unicode__(self):
                return "%s %s %s" % (self.commenter, self.video, self.content)

class Rating(models.Model):
        ratinger = models.ForeignKey(User)
        ONESTAR = 1
        TWOSTARS = 2
        THREESTARS = 3
        FOURSTARS = 4
        FIVESTARS = 5
        RATING_CHOICES = (
                (ONESTAR, 'ONESTAR'),
                (TWOSTARS, 'TWOSTARS'),
                (THREESTARS, 'THREESTARS'),
                (FOURSTARS, 'FOURSTARS'),
                (FIVESTARS, 'FIVESTARS'),
        )
        rating = models.PositiveIntegerField(choices=RATING_CHOICES,
                                             default=THREESTARS)

        def __unicode__(self):
                return "%s %s %s" % (self.ratinger, self.video, self.rating)
        
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
        replies = models.ManyToManyField(Comment, related_name='')
        flags = models.ManyToManyField(Flag, related_name='')

        def __unicode__(self):
                return self.title

# ratings
# related videos
admin.site.register(Comment)
