from django.db import models

# Create your models here.
class Video(models.Model):
        title = models.CharField(max=100)
        uploader = models.ForeignKey(Uploader)
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

class User(models.Model):
        user_name = models.CharField(max_length=30)
        password = models.CharField(max_length=30)
#        email

class uploader(models.Model):
        User = models.ForeignKey(User)
        educational_email = models.CharField(max_length=30)
