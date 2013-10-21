from django.test import TestCase
from videos.models import Video
from django.contrib.auth.models import User

class SearchTest(TestCase):
	def SetUp(self):
		os.system("../manage.py syncdb")
		a = Author(name = "Bob", email = "bob@gmail.com")
		a.save()
		j = Journal(name = "test journal", year=1999, edition=1)
		j.save()
		k1 = Keyword(keyword = "test")
		k2 = Keyword(keyword = "vid")
		k1.save()
		k2.save()
		v = Video(title="testvid", uploader=User.objects.get(username="su"), description = "test video", url=http://google.com, journal

	def SearchExists(self):