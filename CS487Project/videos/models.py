from django.db import models

# Create your models here.
class Author(models.Model):
        name = models.CharField(max_length=50)

class Video(models.Model):
        title = models.CharField(max_length=100)
        #uploader = models.ForeignKey(Video)
        description = models.TextField()
        uploadDate = models.DateField()
        viewCount = models.PositiveIntegerField()
        url = models.URLField()
        authors = models.ForeignKey(Author)
#        keywords = 
#        journal = 
#        year = 
#        edition = 
        #video = models.FileField()
# comments
# flags
# ratings
# related videos

