from django.db import models

# Create your models here.
class Video(models.Model):
        title = models.CharField(max=100)
        uploader = models.ForeignKey(?)
        description = models.TextField()
        uploadDate = models.DateField()
        viewCount = models.PositiveIntegerField
        url = URLField
#        authors = 
#        keywords = 
#        journal = 
#        year = 
#        edition = 
        video = models.FileField()
# comments
# flags
# ratings
# related videos
