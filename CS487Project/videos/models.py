from django.db import models
import datetime

# Create your models here.
class Author(models.Model):
        name = models.CharField(max_length=50)
        email = models.EmailField()

        def __unicode__(self):
                return self.name

class Keyword(models.Model):
        keyword = models.CharField(max_length=100, unique=True)

        def __unicode__(self):
                return self.keyword

class Journal(models.Model):
        name = models.CharField(max_length=100)
        year = models.PositiveIntegerField()
        edition = models.PositiveIntegerField()

        def __unicode__(self):
                return "%s %s %s" % (self.name, self.year, self.edition)

class Video(models.Model):
        title = models.CharField(max_length=100, unique=True)
        #uploader = models.ForeignKey(Video)
        description = models.TextField()
        uploadDate = models.DateField(default=datetime.datetime.now(), editable=False)
        viewCount = models.PositiveIntegerField(default=0)
        url = models.URLField()
        authors = models.ManyToManyField(Author)
        keywords = models.ManyToManyField(Keyword)
        journal = models.ForeignKey(Journal)
        video = models.FileField(upload_to='videos/')

        def __unicode__(self):
                return self.title
# comments
# flags
# ratings
# related videos

